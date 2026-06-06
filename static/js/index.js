        // Utilities
        function linkify(text) {
            if (!text) return "";
            const urlRegex = /(https?:\/\/[^\s]+)/g;
            return text.replace(urlRegex, function(url) {
                return '<a href="' + url + '" target="_blank" rel="noopener noreferrer" style="color:var(--coral); text-decoration:underline;">' + url + '</a>';
            });
        }

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function toggleCandidateProfileEdit(isEditing) {
            const form = document.getElementById('candidate-profile-form');
            if(!form) return;
            const inputs = form.querySelectorAll('input, select, textarea');
            
            // Linkify preview for social_links
            const linksTextarea = document.getElementById('c-links');
            let previewDiv = document.getElementById('c-links-preview');
            if (!previewDiv) {
                previewDiv = document.createElement('div');
                previewDiv.id = 'c-links-preview';
                previewDiv.style.cssText = 'padding: 12px; background: #f8f9ff; border-radius: 12px; font-size: 14px; min-height: 50px; white-space: pre-wrap;';
                linksTextarea.parentNode.insertBefore(previewDiv, linksTextarea.nextSibling);
            }

            inputs.forEach(input => {
                input.readOnly = !isEditing;
                if (!isEditing) {
                    input.style.backgroundColor = '#f8f9ff';
                    input.style.borderColor = 'transparent';
                    input.style.outline = 'none';
                } else {
                    input.style.backgroundColor = '';
                    input.style.borderColor = '';
                }
            });

            if (!isEditing) {
                linksTextarea.style.display = 'none';
                previewDiv.style.display = 'block';
                previewDiv.innerHTML = linkify(linksTextarea.value) || '<i style="color:#999;">No links provided</i>';
            } else {
                linksTextarea.style.display = 'block';
                previewDiv.style.display = 'none';
            }

            document.getElementById('c-save-btn').style.display = isEditing ? 'inline-flex' : 'none';
            document.getElementById('c-edit-btn').style.display = isEditing ? 'none' : 'inline-flex';
        }

        function toggleEmployerProfileEdit(isEditing) {
            const form = document.getElementById('employer-profile-form');
            if(!form) return;
            const inputs = form.querySelectorAll('input, select, textarea');

            // Linkify preview for website_links
            const linksTextarea = document.getElementById('e-links');
            let previewDiv = document.getElementById('e-links-preview');
            if (!previewDiv) {
                previewDiv = document.createElement('div');
                previewDiv.id = 'e-links-preview';
                previewDiv.style.cssText = 'padding: 12px; background: #f8f9ff; border-radius: 12px; font-size: 14px; min-height: 50px; white-space: pre-wrap;';
                linksTextarea.parentNode.insertBefore(previewDiv, linksTextarea.nextSibling);
            }

            inputs.forEach(input => {
                input.readOnly = !isEditing;
                if (!isEditing) {
                    input.style.backgroundColor = '#f8f9ff';
                    input.style.borderColor = 'transparent';
                    input.style.outline = 'none';
                } else {
                    input.style.backgroundColor = '';
                    input.style.borderColor = '';
                }
            });

            if (!isEditing) {
                linksTextarea.style.display = 'none';
                previewDiv.style.display = 'block';
                previewDiv.innerHTML = linkify(linksTextarea.value) || '<i style="color:#999;">No links provided</i>';
            } else {
                linksTextarea.style.display = 'block';
                previewDiv.style.display = 'none';
            }

            document.getElementById('e-save-btn').style.display = isEditing ? 'inline-flex' : 'none';
            document.getElementById('e-edit-btn').style.display = isEditing ? 'none' : 'inline-flex';
        }

        async function apiCall(endpoint, method = 'GET', body = null) {
            let token = getCookie('csrftoken');
            if (!token) {
                const input = document.querySelector('[name=csrfmiddlewaretoken]');
                if (input) token = input.value;
            }
            const headers = {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            };
            const options = { method, headers };
            if (body) options.body = JSON.stringify(body);
            
            const res = await fetch(`/api/${endpoint}`, options);
            if (!res.ok) {
                const err = await res.json().catch(()=>({error: 'API Error'}));
                throw err;
            }
            if (res.status === 204) return null;
            return await res.json();
        }

        // View changing
        function showSection(id) {
            document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function switchAuthTab(type) {
            const tabs = document.querySelectorAll('.tab');
            tabs[0].classList.toggle('active', type === 'login');
            tabs[1].classList.toggle('active', type === 'register');
            document.getElementById('login-form').style.display = type === 'login' ? 'block' : 'none';
            document.getElementById('register-form').style.display = type === 'register' ? 'block' : 'none';
        }

        // State control
        let currentUserRole = null;
        let currentEmployerProfileId = null;
        let authCheckDone = false;

        function homeClick() {
            if (currentUserRole) {
                showSection('home-feed');
                loadFeed();
            } else {
                showSection('landing-page');
            }
        }

        function postJobClick() {
            if (currentUserRole === 'employer') {
                showDashboard();
            } else {
                showSection('auth-section');
            }
        }

        async function findJobNearMeClick() {
            if (currentUserRole === 'candidate') {
                const prof = await apiCall('candidate/profile').catch(() => null);
                if (prof && prof.city) {
                    showSection('home-feed');
                    loadFeed(prof.city);
                } else {
                    alert('Please set your city in your profile first!');
                    showProfile();
                }
            } else if (currentUserRole === 'employer') {
                showSection('auth-section');
                switchAuthTab('register');
            } else {
                showSection('auth-section');
            }
        }

        async function checkAuthAndInit() {
            try {
                // Cache busting with timestamp
                const res = await fetch(`/api/whoami?t=${Date.now()}`, { credentials: 'same-origin' });
                if (res.ok) {
                    const data = await res.json();
                    if (data.role && data.username) {
                        // Pass false to initAppFlow to prevent auto-redirect to feed on load
                        initAppFlow(data.role, data.username, null, false);
                        authCheckDone = true;
                        return;
                    }
                }
            } catch(e) {}

            // Not logged in — show landing page
            document.getElementById('public-nav').style.display = 'flex';
            document.getElementById('user-controls').style.display = 'none';
            showSection('landing-page');
            authCheckDone = true;
        }

        async function logout() {
            try { 
                await apiCall('logout', 'POST'); 
            } catch(e) { 
                console.warn('Server logout failed, clearing local state anyway'); 
            }
            currentUserRole = null;
            // Clear all cookies
            document.cookie.split(";").forEach(function(c) { 
                document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
            });
            
            // Redirect to landing page and force reload to clear app state
            window.location.href = '/';
        }

        function initAppFlow(role, username, redirectTarget = 'home-feed', doRedirect = true) {
            currentUserRole = role;
            document.getElementById('public-nav').style.display = 'none';
            document.getElementById('user-controls').style.display = 'flex';
            document.getElementById('welcome-msg').innerText = username;
            
            // Set avatar circle with initial and role-based color
            const avatarCircle = document.getElementById('nav-avatar-circle');
            if (avatarCircle) {
                avatarCircle.innerText = (username || '?')[0].toUpperCase();
                avatarCircle.classList.remove('role-candidate', 'role-employer');
                avatarCircle.classList.add(role === 'employer' ? 'role-employer' : 'role-candidate');
            }
            
            // If employer, load profile ID for ownership checks
            if (role === 'employer') {
                apiCall('employer/profile').then(p => {
                    currentEmployerProfileId = p.id || null;
                }).catch(() => {});
            }

            if (!doRedirect) return;

            if (redirectTarget === 'profile') {
                showProfile();
            } else {
                showSection('home-feed');
                loadFeed();
            }
        }

        function showDashboard() {
            if (currentUserRole === 'candidate') {
                showSection('candidate-dashboard');
                loadCandidateData();
            } else if (currentUserRole === 'employer') {
                showSection('employer-dashboard');
                loadEmployerData();
            }
        }

        function showProfile() {
            if (currentUserRole === 'candidate') {
                showSection('candidate-profile');
                loadCandidateData();
            } else if (currentUserRole === 'employer') {
                showSection('employer-profile-view');
                loadEmployerData();
            }
        }

        // FEED LOGIC
        let cachedJobsFeed = [];
        let currentFeedTab = 'all';

        function switchFeedTab(tab) {
            currentFeedTab = tab;
            document.getElementById('tab-all-jobs').classList.toggle('active', tab === 'all');
            document.getElementById('tab-recommended').classList.toggle('active', tab === 'recommended');
            renderFeed();
        }

        async function loadFeed(filterCity = null) {
            try {
                if (currentUserRole === 'candidate') {
                    const prof = await apiCall('candidate/profile').catch(() => null);
                    if (!prof || !prof.skills) {
                        alert('You must save your profile details first before viewing the feed!');
                        showSection('candidate-dashboard');
                        loadCandidateData();
                        return;
                    }
                    window.currentCandidateSkills = prof.skills;
                    window.currentCandidateCity = prof.city;
                    document.getElementById('feed-tabs').style.display = 'flex';
                } else if (currentUserRole === 'employer') {
                    const prof = await apiCall('employer/profile').catch(() => null);
                    if (!prof || !prof.company_name) {
                        alert('You must save your company details first before viewing the feed!');
                        showSection('employer-dashboard');
                        loadEmployerData();
                        return;
                    }
                    window.currentEmployerProfileId = prof.id;
                    document.getElementById('feed-tabs').style.display = 'none';
                } else {
                    document.getElementById('feed-tabs').style.display = 'none';
                }

                const endpoint = filterCity ? `jobs/feed?city=${encodeURIComponent(filterCity)}` : 'jobs/feed';
                cachedJobsFeed = await apiCall(endpoint);
                renderFeed();
                if (filterCity) {
                   // Highlight that we are filtering
                   const feedTitle = document.querySelector('#home-feed h2');
                   if (feedTitle) feedTitle.innerText = `📍 Jobs in ${filterCity}`;
                } else {
                   const feedTitle = document.querySelector('#home-feed h2');
                   if (feedTitle) feedTitle.innerText = `🔥 Global Jobs Feed`;
                }
            } catch(e) { console.error('Error loading feed', e); }
        }

        function renderFeed() {
            const list = document.getElementById('all-jobs-feed');
            list.innerHTML = '';
            
            let jobsToRender = cachedJobsFeed;
            if (currentUserRole === 'candidate' && currentFeedTab === 'recommended') {
                const cSkills = window.currentCandidateSkills.toLowerCase().split(',').map(s => s.trim()).filter(Boolean);
                jobsToRender = cachedJobsFeed.filter(j => {
                    const jSkills = (j.required_skills || '').toLowerCase().split(',').map(s => s.trim()).filter(Boolean);
                    return cSkills.some(cs => jSkills.includes(cs));
                });
            }

            if(jobsToRender.length === 0) {
                list.innerHTML = '<p style="text-align:center; color: #666;">No jobs found in this category.</p>';
                return;
            }
            
            jobsToRender.forEach(j => {
                const applyBtnHtml = currentUserRole === 'candidate' 
                    ? `<button class="jc-apply" onclick="applyJob(${j.id})">Apply to Job</button>` 
                    : '';
                const salaryStr = j.salary ? `₹${Number(j.salary).toLocaleString('en-IN')}/month` : 'N/A';
                const aiSalaryHtml = currentUserRole === 'candidate' && j.salary ? 
                    `<button class="jc-apply" style="background:var(--yellow); color:var(--dark);" onclick="checkSalary(${j.id})">✨ Assess Salary</button>` : '';
                
                list.innerHTML += `
                    <div class="job-card">
                        <div class="jc-top">
                            <button class="jc-logo jcl-1" style="border:none; cursor:pointer;" onclick="viewCompanyProfile(${j.id})" title="View Company Profile">💼</button>
                            <div class="jc-info">
                                <h3 style="margin-bottom:4px;font-family:'Nunito',sans-serif;font-weight:800;font-size:16px;">${j.title}</h3>
                                <span style="font-size:13px;color:#999;">${j.company_name || 'N/A'} • ${j.city || 'N/A'} (Pin: ${j.pincode})</span>
                            </div>
                        </div>
                        <div class="jc-tags" style="margin-bottom:12px;">
                            <span class="pj-tag pj-tag-a">💰 ${salaryStr}</span>
                            ${j.is_walk_in ? '<span class="pj-tag pj-tag-b">🚶 Walk-In</span>' : ''}
                        </div>
                        <div style="font-size:13px; color:#666; margin-bottom:12px; padding:10px; background:var(--offwhite); border-radius:12px;">
                            <strong>Skills Needed:</strong> ${j.required_skills}
                            ${j.is_walk_in && j.walk_in_address ? `<div style="font-size:12px; margin-top:8px; padding:8px; background:#E8F5E9; border-radius:8px; color:#1b8c4f;">📍 <strong>Walk-In:</strong> ${j.walk_in_address}</div>` : ''}
                            ${j.expires_at ? `<div style="font-size:12px; margin-top:8px; color:var(--coral);">⏰ <strong>Expires:</strong> ${new Date(j.expires_at).toLocaleString()}</div>` : ''}
                        </div>
                        <div class="jc-footer" style="justify-content: flex-start; gap: 8px; flex-wrap:wrap;">
                            ${applyBtnHtml}
                            ${aiSalaryHtml}
                            ${currentUserRole === 'candidate' ? `<button class="jc-apply" style="background:var(--purple); color:white;" onclick="generateLearningPath(${j.id})">📚 AI Learning Path</button>` : ''}
                        </div>
                    </div>
                `;
            });
        }

        // Auth Forms
        document.getElementById('login-form').onsubmit = async (e) => {
            e.preventDefault();
            try {
                const res = await apiCall('login', 'POST', {
                    username: e.target.elements[0].value,
                    password: e.target.elements[1].value
                });
                initAppFlow(res.role, e.target.elements[0].value);
            } catch (err) { alert(err.error || 'Invalid credentials'); }
        };

        document.getElementById('register-form').onsubmit = async (e) => {
            e.preventDefault();
            const btn = e.target.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.innerText = '⏳ Creating...';
            try {
                const role = e.target.elements[0].value;
                const username = e.target.elements[1].value;
                const password = e.target.elements[3].value;
                
                await apiCall('register', 'POST', {
                    role: role,
                    username: username,
                    email: e.target.elements[2].value,
                    password: password
                });
                
                // Auto-login
                const loginRes = await apiCall('login', 'POST', {
                    username: username,
                    password: password
                });
                
                // Redirect immediately to Profile section
                initAppFlow(loginRes.role, username, 'profile');
                alert('Registered successfully! Please complete your profile.');
            } catch (err) { alert(err.error || JSON.stringify(err)); }
            finally {
                btn.disabled = false;
                btn.innerText = '🎉 Create Account';
            }
        };

        // CANDIDATE dashboard logic — shows applied count + applied jobs list + profile form
        async function loadCandidateData() {
            try {
                // Load applications
                const apps = await apiCall('candidate/applications');
                document.getElementById('c-stat-applied').innerText = apps.length;
                const appList = document.getElementById('applied-jobs-list');
                if (!apps || apps.length === 0) {
                    appList.innerHTML = '<div style="text-align:center; padding:32px 0;"><div style="font-size:48px; margin-bottom:12px;">📭</div><p style="color:#999; font-weight:600;">No applications yet.</p><p style="color:#bbb; font-size:13px; margin-top:4px;">Browse the feed and hit Apply on a job!</p></div>';
                } else {
                    appList.innerHTML = apps.map(a => {
                        const statusColor = a.status === 'Shortlisted' ? 'var(--green)' : a.status === 'Rejected' ? 'var(--coral)' : 'var(--purple)';
                        const salaryStr = a.salary ? `₹${Number(a.salary).toLocaleString('en-IN')}/month` : 'N/A';
                        return `
                            <div style="border:2px solid #F0F0F8; border-radius:16px; padding:18px; margin-bottom:12px; transition:.2s;" onmouseover="this.style.borderColor='var(--coral)'" onmouseout="this.style.borderColor='#F0F0F8'">
                                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                                    <div>
                                        <div style="font-family:'Nunito',sans-serif; font-weight:800; font-size:16px; color:var(--dark);">${a.job_title}</div>
                                        <div style="font-size:13px; color:#999; margin-top:3px;">${a.company_name} &bull; Pin: ${a.pincode}</div>
                                    </div>
                                    <span style="background:${statusColor}22; color:${statusColor}; font-size:12px; font-weight:800; padding:5px 14px; border-radius:20px; white-space:nowrap;">${a.status}</span>
                                </div>
                                <div style="display:flex; gap:20px; margin-top:12px; font-size:13px; color:#666; flex-wrap:wrap;">
                                    <span>💰 ${salaryStr}</span>
                                    <span>🎯 Match: <strong>${a.match_score}%</strong></span>
                                    <span>📅 ${a.applied_at}</span>
                                </div>
                                <div style="margin-top:10px; padding:12px; background: ${a.status === 'Shortlisted' ? 'rgba(16, 185, 129, 0.1)' : 'var(--offwhite)'}; border-radius:12px; font-size:13px; color: ${a.status === 'Shortlisted' ? 'var(--dark)' : '#666'}; border: 1px dashed ${a.status === 'Shortlisted' ? 'var(--green)' : '#ccc'};">
                                    ${a.status === 'Shortlisted' ? 
                                        `<strong>HR Name:</strong> ${a.contact_name || 'N/A'} | <strong>Call:</strong> ${a.contact_phone || 'N/A'} | <strong>Email:</strong> ${a.contact_email || 'N/A'}
                                         <div style="margin-top:8px;"><strong>Links:</strong> ${linkify(a.website_links) || 'N/A'}</div>` : 
                                        `<span style="display:flex; align-items:center; gap:6px; color:#999;">🔒 <i>HR details will be unlocked once you are Shortlisted by the employer.</i></span>`
                                    }
                                </div>
                            </div>`;
                    }).join('');
                }

                // Load candidate profile
                const profile = await apiCall('candidate/profile');
                if (profile) {
                    document.getElementById('c-skills').value = profile.skills || '';
                    document.getElementById('c-experience').value = profile.experience || 0;
                    document.getElementById('c-pincode').value = profile.pincode || '';
                    document.getElementById('c-city').value = profile.city || '';
                    document.getElementById('c-phone').value = profile.phone || '';
                    document.getElementById('c-contact-email').value = profile.contact_email || '';
                    document.getElementById('c-about').value = profile.about || '';
                    document.getElementById('c-links').value = profile.social_links || '';
                    window.currentCandidateSkills = profile.skills;
                    
                    if (profile.skills) {
                        toggleCandidateProfileEdit(false);
                    } else {
                        toggleCandidateProfileEdit(true);
                    }
                    
                    if (profile.resume_ats_score || profile.resume_file) {
                        document.getElementById('resume-analysis-result').style.display = 'block';
                        document.getElementById('ra-score').innerText = `Score: ${profile.resume_ats_score || 0}/100`;
                        document.getElementById('ra-exp').innerText = profile.resume_experience || 0;
                        document.getElementById('ra-skills').innerText = profile.resume_parsed_skills || 'None extracted';
                        document.getElementById('ra-summary').innerText = profile.resume_summary || 'No summary available.';
                        if (profile.resume_file) {
                            document.getElementById('ra-download-btn').href = profile.resume_file;
                            document.getElementById('ra-download-btn').style.display = 'block';
                        } else {
                            document.getElementById('ra-download-btn').style.display = 'none';
                        }
                    } else {
                        document.getElementById('resume-analysis-result').style.display = 'none';
                    }
                } else {
                    toggleCandidateProfileEdit(true);
                }
            } catch (err) {
                console.error('Failed to load candidate data', err);
            }
        }

        document.getElementById('candidate-profile-form').onsubmit = async (e) => {
            e.preventDefault();
            try {
                await apiCall('candidate/profile', 'POST', {
                    skills: document.getElementById('c-skills').value,
                    experience: document.getElementById('c-experience').value,
                    pincode: document.getElementById('c-pincode').value,
                    city: document.getElementById('c-city').value,
                    phone: document.getElementById('c-phone').value,
                    contact_email: document.getElementById('c-contact-email').value,
                    about: document.getElementById('c-about').value,
                    social_links: document.getElementById('c-links').value
                });
                alert('Profile updated successfully!');
                window.scrollTo({ top: 0, behavior: 'smooth' });
                toggleCandidateProfileEdit(false);
                loadCandidateData();
            } catch (err) { alert('Error updating profile'); }
        };

        document.getElementById('candidate-resume-form').onsubmit = async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('r-resume-file');
            if (fileInput.files.length === 0) return;
            
            const btn = document.getElementById('r-upload-btn');
            const originalText = btn.innerText;
            btn.innerText = '⏳ Analyzing...';
            btn.disabled = true;

            let token = getCookie('csrftoken');
            if (!token) {
                const input = document.querySelector('[name=csrfmiddlewaretoken]');
                if (input) token = input.value;
            }

            const formData = new FormData();
            formData.append('resume_file', fileInput.files[0]);

            try {
                const res = await fetch('/api/candidate/resume/analyze', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': token
                    },
                    body: formData
                });
                
                const data = await res.json();
                
                if (!res.ok) {
                    alert(data.error || 'Failed to analyze resume');
                } else {
                    alert('Resume analyzed successfully!');
                    loadCandidateData(); // refresh
                }
            } catch(error) {
                alert('Connection error while analyzing resume.');
            } finally {
                btn.innerText = originalText;
                btn.disabled = false;
            }
        };

        async function applyJob(id) {
            try {
                const res = await apiCall('candidate/apply', 'POST', { job_id: id });
                alert(`Applied successfully!\nYour ranking has been sent to the employer.`);
                // Refresh dashboard stats if visible
                if (document.getElementById('candidate-dashboard').classList.contains('active')) {
                    loadCandidateData();
                }
            } catch (err) { alert('Error applying to job (maybe you already applied?)'); }
        }

        // EMPLOYER dashboard logic
        async function loadEmployerData() {
            try {
                // profile
                const profile = await apiCall('employer/profile');
                if (profile && profile.id) {
                    window.currentEmployerProfileId = profile.id;
                    document.getElementById('e-company').value = profile.company_name || '';
                    document.getElementById('e-pincode').value = profile.pincode || '';
                    document.getElementById('e-city').value = profile.city || '';
                    document.getElementById('e-contact-name').value = profile.contact_name || '';
                    document.getElementById('e-contact-phone').value = profile.contact_phone || '';
                    document.getElementById('e-contact-email').value = profile.contact_email || '';
                    document.getElementById('e-about').value = profile.about || '';
                    document.getElementById('e-links').value = profile.website_links || '';
                    document.getElementById('e-org-details').value = profile.org_details || '';
                    
                    if (profile.company_name) {
                        toggleEmployerProfileEdit(false);
                    } else {
                        toggleEmployerProfileEdit(true);
                    }
                } else {
                    toggleEmployerProfileEdit(true);
                }

                // posted jobs
                const jobs = await apiCall('employer/jobs');
                
                document.getElementById('e-stat-jobs').innerText = jobs.length;
                const totalApplicants = jobs.reduce((sum, job) => sum + (job.applicants_count || 0), 0);
                document.getElementById('e-stat-applicants').innerText = totalApplicants;
                
                const list = document.getElementById('posted-jobs-list');
                list.innerHTML = '';
                if(jobs.length === 0) {
                    list.innerHTML = '<p>You have not posted any jobs yet.</p>';
                }
                jobs.forEach(j => {
                    const eSalaryStr = j.salary ? `₹${Number(j.salary).toLocaleString('en-IN')}/month` : 'N/A';
                    list.innerHTML += `
                        <div class="job-card">
                            <div class="jc-top">
                                <div class="jc-logo jcl-3">🏢</div>
                                <div class="jc-info">
                                    <h3 style="margin-bottom:4px;font-family:'Nunito',sans-serif;font-weight:800;font-size:16px;">${j.title}</h3>
                                    <span style="font-size:13px;color:#999;">Pin: ${j.pincode}</span>
                                </div>
                            </div>
                            <div class="jc-tags" style="margin-bottom:12px;">
                                <span class="pj-tag pj-tag-a">💰 ${eSalaryStr}</span>
                                ${j.is_walk_in ? '<span class="pj-tag pj-tag-b">🚶 Walk-In</span>' : ''}
                            </div>
                            <div style="font-size:13px; color:#666; margin-bottom:12px; padding:10px; background:var(--offwhite); border-radius:12px;">
                                <strong>Expected Skills:</strong> ${j.required_skills}<br>
                                <strong>Total Applicants:</strong> ${j.applicants_count || 0}
                                ${j.is_walk_in && j.walk_in_address ? `<div style="font-size:12px; margin-top:8px; padding:8px; background:#E8F5E9; border-radius:8px; color:#1b8c4f;">📍 <strong>Walk-In:</strong> ${j.walk_in_address}</div>` : ''}
                                ${j.expires_at ? `<div style="font-size:12px; margin-top:8px; color:var(--coral);">⏰ <strong>Auto-Delete at:</strong> ${new Date(j.expires_at).toLocaleString()}</div>` : ''}
                            </div>
                            <div class="jc-footer" style="justify-content: flex-start; gap: 8px; flex-wrap:wrap;">
                                <button class="jc-apply" onclick="viewCandidates(${j.id}, '${j.title}')">View Ranked Candidates (${j.applicants_count || 0})</button>
                                <button class="jc-apply" style="background:var(--yellow); color:var(--dark);" onclick="editJob(${j.id}, '${(j.title || '').replace(/'/g,"\\'")}', '${(j.required_skills || '').replace(/'/g,"\\'")}', '${j.pincode}', '${(j.city || '').replace(/'/g,"\\'")}', ${j.salary || 0}, ${j.is_walk_in || false}, '${(j.walk_in_address || '').replace(/'/g,"\\'")}')">✏️ Edit Job</button>
                            </div>
                        </div>
                    `;
                });
            } catch (err) {}
        }

        document.getElementById('employer-profile-form').onsubmit = async (e) => {
            e.preventDefault();
            try {
                await apiCall('employer/profile', 'POST', {
                    company_name: document.getElementById('e-company').value,
                    pincode: document.getElementById('e-pincode').value,
                    city: document.getElementById('e-city').value,
                    contact_name: document.getElementById('e-contact-name').value,
                    contact_phone: document.getElementById('e-contact-phone').value,
                    contact_email: document.getElementById('e-contact-email').value,
                    about: document.getElementById('e-about').value,
                    website_links: document.getElementById('e-links').value,
                    org_details: document.getElementById('e-org-details').value
                });
                alert('Company Profile saved!');
                window.scrollTo({ top: 0, behavior: 'smooth' });
                toggleEmployerProfileEdit(false);
            } catch (err) { alert('Error saving profile'); }
        };

        document.getElementById('post-job-form').onsubmit = async (e) => {
            e.preventDefault();
            const salaryVal = document.getElementById('j-salary').value;
            if (!salaryVal || Number(salaryVal) <= 0) {
                alert('Please enter a valid salary before posting the job.');
                return;
            }
            try {
                const isWalkIn = document.getElementById('j-walk-in').checked;
                await apiCall('employer/job', 'POST', {
                    title: document.getElementById('j-title').value,
                    required_skills: document.getElementById('j-skills').value,
                    pincode: document.getElementById('j-pincode').value,
                    city: document.getElementById('j-city').value,
                    salary: salaryVal,
                    is_walk_in: isWalkIn,
                    walk_in_address: isWalkIn ? document.getElementById('j-walk-in-address').value : '',
                    timer_value: document.getElementById('j-timer-value').value,
                    timer_unit: document.getElementById('j-timer-unit').value
                });
                alert('Job Posted to the Global Feed!');
                e.target.reset();
                document.getElementById('j-walk-in-addr-group').style.display = 'none';
                document.getElementById('j-timer-value').value = 0;
                document.getElementById('j-timer-unit').value = 'hours';
                loadEmployerData();
            } catch (err) { alert('Error posting job'); }
        };

        // RANKED CANDIDATES logic
        let currentJobCandidates = [];
        let currentCandidateTab = 'recommended';
        let currentViewJobId = null;
        let currentViewJobTitle = '';

        async function viewCandidates(jobId, title) {
            currentViewJobId = jobId;
            currentViewJobTitle = title;
            currentCandidateTab = 'recommended'; 
            showSection('ranked-candidates');
            document.getElementById('rc-job-title').innerText = `Candidates for: ${title}`;
            
            // Reset tabs
            document.getElementById('tab-recommended-candidates').classList.add('active');
            document.getElementById('tab-all-candidates').classList.remove('active');

            try {
                currentJobCandidates = await apiCall(`employer/job/${jobId}/ranked-candidates`);
                renderCandidatesList();
            } catch (err) { alert('Error loading candidates'); }
        }

        function switchCandidateTab(tab) {
            currentCandidateTab = tab;
            document.getElementById('tab-recommended-candidates').classList.toggle('active', tab === 'recommended');
            document.getElementById('tab-all-candidates').classList.toggle('active', tab === 'all');
            renderCandidatesList();
        }

        function renderCandidatesList() {
            const list = document.getElementById('candidates-list');
            list.innerHTML = '';
            
            let filtered = currentJobCandidates;
            if (currentCandidateTab === 'recommended') {
                // Filter logic: match_score >= 50 as Recommended
                filtered = currentJobCandidates.filter(c => (c.match_score || 0) >= 50);
            }

            if(filtered.length === 0) {
                const msg = currentCandidateTab === 'recommended' 
                    ? 'No candidates meet the recommendation threshold (50%) yet. Try checking "All Applicants".' 
                    : 'No candidates have applied yet.';
                list.innerHTML = `<p style="text-align:center; padding:32px; color:#666;">${msg}</p>`;
                return;
            }

            filtered.forEach(app => {
                let stColor = app.status === 'Shortlisted' ? '#10b981' : (app.status === 'Rejected' ? '#ef4444' : '#f59e0b');
                list.innerHTML += `
                    <div class="job-card" style="border-left: 6px solid ${stColor};">
                        <div class="jc-top">
                            <button class="jc-logo jcl-2" style="border:none; cursor:pointer;" onclick="viewCandidateProfile(${app.id})" title="View Candidate Profile">👨‍🔧</button>
                            <div class="jc-info" style="width:100%;">
                                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                    <h3 style="margin-bottom:4px;font-family:'Nunito',sans-serif;font-weight:800;font-size:16px;">${app.candidate_name}</h3>
                                    <span class="pj-tag pj-tag-b" style="background:${stColor}; font-size:12px;">Match: ${app.match_score.toFixed(2)}%</span>
                                </div>
                                <span style="font-size:13px;color:#999;">Applied on: ${new Date(app.created_at).toLocaleDateString()}</span>
                            </div>
                        </div>
                        <div style="font-size:13px; color:#666; margin-bottom:12px; padding:10px; background:var(--offwhite); border-radius:12px;">
                            <strong>Skills:</strong> ${app.candidate_skills}<br/>
                            <strong>Exp:</strong> ${app.candidate_experience || 0} yrs &bull; <strong>Pin:</strong> ${app.candidate_pincode || 'N/A'}<br/>
                            <strong>Contact:</strong> ${app.candidate_phone || 'No phone'} | ${app.candidate_contact_email || 'No email'}<br/>
                            <strong>Portfolio/Links:</strong> ${linkify(app.candidate_social_links) || 'N/A'}<br/>
                            Status: <strong style="color: ${stColor}">${app.status}</strong>
                        </div>
                        <div class="jc-footer" style="justify-content: flex-start; gap: 8px;">
                            <button class="jc-apply" style="background:#10b981; color:white;" onclick="updateStatus(${app.id}, 'Shortlisted', ${currentViewJobId}, '${currentViewJobTitle.replace(/'/g, "\\'")}')">Shortlist</button>
                            <button class="jc-apply" style="background:#ef4444; color:white;" onclick="updateStatus(${app.id}, 'Rejected', ${currentViewJobId}, '${currentViewJobTitle.replace(/'/g, "\\'")}')">Reject</button>
                        </div>
                    </div>
                `;
            });
        }

        async function updateStatus(appId, status, jobId, title) {
            try {
                await apiCall(`employer/application/${appId}/status`, 'PATCH', { status });
                viewCandidates(jobId, title); // Refresh the list
            } catch (err) { alert('Error updating status'); }
        }

        // EDIT JOB logic
        let editingJobId = null;

        async function editJob(id, title, skills, pincode, city, salary, is_walk_in, walk_in_address) {
            editingJobId = id;
            document.getElementById('edit-j-title').value = title || '';
            document.getElementById('edit-j-skills').value = skills || '';
            document.getElementById('edit-j-pincode').value = pincode || '';
            document.getElementById('edit-j-city').value = city || '';
            document.getElementById('edit-j-salary').value = salary || 0;
            const walkInCheck = document.getElementById('edit-j-walk-in');
            walkInCheck.checked = !!is_walk_in;
            document.getElementById('edit-j-walk-in-addr-group').style.display = is_walk_in ? 'block' : 'none';
            document.getElementById('edit-j-walk-in-address').value = walk_in_address || '';
            
            // Default reset for timer
            document.getElementById('edit-j-timer-value').value = 0;
            document.getElementById('edit-j-timer-unit').value = 'hours';
            document.getElementById('edit-j-current-expiry-group').style.display = 'none';

            try {
                const jobData = await apiCall(`employer/job/${id}/edit`, 'GET').catch(() => null);
                if (jobData) {
                    document.getElementById('edit-j-title').value = jobData.title || '';
                    document.getElementById('edit-j-skills').value = jobData.required_skills || '';
                    document.getElementById('edit-j-pincode').value = jobData.pincode || '';
                    document.getElementById('edit-j-city').value = jobData.city || '';
                    document.getElementById('edit-j-salary').value = jobData.salary || 0;
                    walkInCheck.checked = !!jobData.is_walk_in;
                    document.getElementById('edit-j-walk-in-addr-group').style.display = jobData.is_walk_in ? 'block' : 'none';
                    document.getElementById('edit-j-walk-in-address').value = jobData.walk_in_address || '';
                    
                    if (jobData.expires_at) {
                        const expiryDate = new Date(jobData.expires_at);
                        document.getElementById('edit-j-current-expiry').innerText = expiryDate.toLocaleString();
                        document.getElementById('edit-j-current-expiry-group').style.display = 'block';
                    }
                }
            } catch(err) { console.error('Failed to load job for editing', err); }
            try {
                const modal = document.getElementById('edit-job-modal');
                if (modal) modal.style.display = 'flex';
            } catch(e) { console.error('Modal failed to open', e); }
        }

        function closeEditModal() {
            document.getElementById('edit-job-modal').style.display = 'none';
            editingJobId = null;
        }

        async function deleteJob() {
            if (!editingJobId) return;
            if (!confirm('Are you sure you want to delete this job? This action cannot be undone.')) return;
            try {
                await apiCall(`employer/job/${editingJobId}/edit`, 'DELETE');
                alert('Job deleted successfully!');
                closeEditModal();
                loadFeed();
                if (currentUserRole === 'employer') loadEmployerData();
            } catch (err) { alert('Error deleting job: ' + (err.error || JSON.stringify(err))); }
        }

        document.getElementById('edit-job-form').onsubmit = async (e) => {
            e.preventDefault();
            if (!editingJobId) return;
            try {
                const editWalkIn = document.getElementById('edit-j-walk-in').checked;
                await apiCall(`employer/job/${editingJobId}/edit`, 'PATCH', {
                    title: document.getElementById('edit-j-title').value,
                    required_skills: document.getElementById('edit-j-skills').value,
                    pincode: document.getElementById('edit-j-pincode').value,
                    city: document.getElementById('edit-j-city').value,
                    salary: document.getElementById('edit-j-salary').value,
                    is_walk_in: editWalkIn,
                    walk_in_address: editWalkIn ? document.getElementById('edit-j-walk-in-address').value : '',
                    timer_value: document.getElementById('edit-j-timer-value').value,
                    timer_unit: document.getElementById('edit-j-timer-unit').value
                });
                alert('Job updated successfully!');
                closeEditModal();
                loadFeed();
                if (currentUserRole === 'employer') loadEmployerData();
            } catch (err) { alert('Error updating job: ' + (err.error || JSON.stringify(err))); }
        };

        // AI FEATURES logic
        function showAILoading(title) {
            document.getElementById('ai-modal').style.display = 'flex';
            document.getElementById('ai-modal-title').innerHTML = title;
            document.getElementById('ai-modal-content').innerHTML = `
                <div style="text-align:center; padding: 2rem;">
                    <div style="display:inline-block; border: 4px solid rgba(139, 92, 246, 0.3); border-top: 4px solid #8b5cf6; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite;"></div>
                    <p style="margin-top: 1rem; color: #666;">Wait for a moment...</p>
                </div>
            `;
        }

        async function checkSalary(jobId) {
            showAILoading('✨ AI Salary Fairness Check');
            try {
                const timeoutPromise = new Promise((_, reject) => 
                    setTimeout(() => reject({ error: 'No Internet Connection', isTimeout: true }), 600000)
                );
                const res = await Promise.race([
                    apiCall(`candidate/job/${jobId}/salary-check`, 'GET'),
                    timeoutPromise
                ]);
                if (res.error) {
                    document.getElementById('ai-modal-content').innerHTML = `<p style="color:#ef4444;">Error: ${res.message || res.error}</p>`;
                    return;
                }
                
                let statusColor = '#10b981'; // Green for Fair/Excellent
                if (res.status === 'Below Average') statusColor = '#f59e0b';
                if (res.status === 'Poor' || res.status === 'Unfair') statusColor = '#ef4444';

                document.getElementById('ai-modal-content').innerHTML = `
                    <div style="text-align:center; margin-bottom: 2rem;">
                        <h2 style="color: ${statusColor}; font-size: 2rem; margin-bottom: 0.5rem;">${res.status}</h2>
                        <p style="color: #666; font-size: 1.1rem;">Estimated Market Range: <strong>${res.market_range || 'Unknown'}</strong></p>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 12px; border-left: 4px solid ${statusColor};">
                        <p style="line-height: 1.6;">${res.explanation}</p>
                    </div>
                `;
            } catch (err) {
                if (err.isTimeout) {
                    alert("No Internet Connection");
                    document.getElementById('ai-modal').style.display = 'none';
                } else {
                    document.getElementById('ai-modal-content').innerHTML = `<p style="color:#ef4444;">Failed to fetch salary assessment. Ensure your profile is complete.</p>`;
                }
            }
        }

        async function generateLearningPath(jobId) {
            showAILoading('📚 Personalized Learning Path');
            try {
                const timeoutPromise = new Promise((_, reject) => 
                    setTimeout(() => reject({ error: 'No Internet Connection', isTimeout: true }), 600000)
                );
                const res = await Promise.race([
                    apiCall(`candidate/job/${jobId}/learning-path`, 'POST'),
                    timeoutPromise
                ]);
                if (res.error) {
                    document.getElementById('ai-modal-content').innerHTML = `<p style="color:#ef4444;">Error: ${res.message || res.error}</p>`;
                    return;
                }

                let roadmapHtml = '';
                if (res.roadmap && res.roadmap.length > 0) {
                    res.roadmap.forEach((item, idx) => {
                        roadmapHtml += `
                            <div style="background: rgba(255,255,255,0.05); margin-bottom: 1rem; padding: 1.25rem; border-radius: 12px; position:relative;">
                                <div style="position:absolute; top:-10px; left:-10px; background:#8b5cf6; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;">${idx+1}</div>
                                <h4 style="color: #c084fc; margin-bottom: 0.5rem; margin-left:1rem;">${item.topic}</h4>
                                <p style="font-size: 0.9rem; margin-left:1rem; margin-bottom:0.5rem;"><strong>Focus:</strong> ${item.focus_area}</p>
                                <div style="display:flex; justify-content:space-between; margin-left:1rem; font-size: 0.85rem; color: #666;">
                                    <span>⏱️ ${item.estimated_time}</span>
                                    <span>🔗 ${item.resource_suggestion}</span>
                                </div>
                            </div>
                        `;
                    });
                } else {
                    roadmapHtml = `<p style="text-align:center; color:#10b981;">Great news! You already have all the required skills for this job.</p>`;
                }

                document.getElementById('ai-modal-content').innerHTML = `
                    <p style="margin-bottom: 1.5rem; line-height: 1.6; color: #666;">
                        <strong>Analysis:</strong> ${res.gap_analysis}
                    </p>
                    <div>
                        ${roadmapHtml}
                    </div>
                `;
            } catch (err) {
                if (err.isTimeout) {
                    alert("No Internet Connection");
                    document.getElementById('ai-modal').style.display = 'none';
                } else {
                    document.getElementById('ai-modal-content').innerHTML = `<p style="color:#ef4444;">Failed to generate learning path. Ensure your profile has skills listed.</p>`;
                }
            }
        }

        // INIT
        checkAuthAndInit();

        // Company Profile logic
        async function viewCompanyProfile(jobId) {
            document.getElementById('company-profile-modal').style.display = 'flex';
            document.getElementById('company-profile-content').innerHTML = '<div style="text-align:center; padding: 2rem;"><p style="color:#666;">Loading profile...</p></div>';
            try {
                const res = await apiCall(`job/${jobId}/employer`);
                if (res.error) {
                    document.getElementById('company-profile-content').innerHTML = `<p style="color:var(--coral); text-align:center;">${res.error}</p>`;
                    return;
                }
                
                let html = `
                    <div style="margin-bottom: 16px;">
                        <h4 style="font-size: 20px; font-weight: 800; margin-bottom: 4px;">${res.company_name || 'N/A'}</h4>
                        <div style="color: #666; font-size: 14px;">📍 ${res.city || 'No city'} &bull; Pin: ${res.pincode || 'N/A'}</div>
                    </div>
                `;
                html += `<div style="margin-bottom: 16px;"><strong>About:</strong><p style="margin-top: 4px; font-size: 14px; color: #444;">${res.about || 'Not provided'}</p></div>`;
                html += `<div style="margin-bottom: 16px;"><strong>Organisation Details:</strong><p style="margin-top: 4px; font-size: 14px; color: #444;">${res.org_details || 'Not provided'}</p></div>`;
                html += `<div style="margin-bottom: 16px;"><strong>Website/Social:</strong><div style="margin-top: 4px; font-size: 14px;">${res.website_links ? linkify(res.website_links) : 'Not provided'}</div></div>`;
                
                if (res.contact_name || res.contact_phone || res.contact_email) {
                    html += `<div style="margin-top: 24px; padding: 12px; background: rgba(16, 185, 129, 0.1); border: 1px dashed var(--green); border-radius: 12px;">
                        <p style="color: var(--green); margin-bottom: 8px; font-weight: 800;">🔓 Shortlisted Contact Details</p>
                        <div style="font-size: 14px;">
                            <strong>HR Name:</strong> ${res.contact_name || 'N/A'} <br>
                            <strong>Phone:</strong> ${res.contact_phone || 'N/A'} <br>
                            <strong>Email:</strong> ${res.contact_email || 'N/A'}
                        </div>
                    </div>`;
                } else {
                    html += `<div style="margin-top: 24px; padding: 12px; background: var(--offwhite); border: 1px dashed #ccc; border-radius: 12px; font-size: 13px; color: #999;">
                        🔒 <i>HR Contact details are hidden. They will be unlocked if you are Shortlisted by this employer.</i>
                    </div>`;
                }
                
                document.getElementById('company-profile-content').innerHTML = html;
            } catch(err) {
                document.getElementById('company-profile-content').innerHTML = `<p style="color:var(--coral); text-align:center;">Failed to load company profile.</p>`;
            }
        }

        // Candidate Profile logic (Employer view)
        function viewCandidateProfile(appId) {
            const app = currentJobCandidates.find(a => a.id === appId);
            if(!app) return;
            
            document.getElementById('candidate-profile-modal').style.display = 'flex';
            
            let stColor = app.status === 'Shortlisted' ? '#10b981' : (app.status === 'Rejected' ? '#ef4444' : '#f59e0b');
            
            let html = `
                <div style="margin-bottom: 16px;">
                    <h4 style="font-size: 20px; font-weight: 800; margin-bottom: 4px;">${app.candidate_name || 'N/A'}</h4>
                    <div style="color: #666; font-size: 14px;">📍 ${app.candidate_city || 'No city'} &bull; Pin: ${app.candidate_pincode || 'N/A'}</div>
                </div>
                <div style="margin-bottom: 16px;">
                    <strong>Experience:</strong>
                    <p style="margin-top: 4px; font-size: 14px; color: #444;">${app.candidate_experience || 0} years</p>
                </div>
                <div style="margin-bottom: 16px;">
                    <strong>Skills:</strong>
                    <p style="margin-top: 4px; font-size: 14px; color: #444;">${app.candidate_skills || 'N/A'}</p>
                </div>
                <div style="margin-bottom: 16px;">
                    <strong>Portfolio/Links:</strong>
                    <div style="margin-top: 4px; font-size: 14px;">${linkify(app.candidate_social_links) || 'N/A'}</div>
                </div>

                ${app.candidate_resume_ats_score || app.candidate_resume_file ? `
                <div style="margin-bottom: 16px; padding: 16px; border-radius: 12px; background: rgba(142, 45, 226, 0.05); border: 1px solid rgba(142, 45, 226, 0.2);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
                        <h4 style="font-family:'Nunito',sans-serif;font-weight:800;font-size:16px;margin:0;color:var(--purple);">✨ AI Resume Analysis</h4>
                        <span style="font-weight:900; background:var(--purple); color:white; padding:4px 12px; border-radius:20px; font-size:14px;">ATS Score: ${app.candidate_resume_ats_score || 0}/100</span>
                    </div>
                    <strong>Summary:</strong>
                    <p style="margin-top: 4px; font-size: 14px; color: #444; line-height:1.5;">${app.candidate_resume_summary || 'No summary available.'}</p>
                    ${app.candidate_resume_file ? `<a href="${app.candidate_resume_file}" target="_blank" class="btn btn-outline" style="display:block; text-align:center; margin-top:16px; padding:8px; font-size:14px;">⬇️ View Original Resume</a>` : ''}
                </div>
                ` : `
                <div style="margin-bottom: 16px; padding: 12px; background: var(--offwhite); border-radius: 12px; font-size: 13px; color: #999;">
                    📄 No uploaded resume for this candidate.
                </div>
                `}
                
                <div style="margin-top: 24px; padding: 12px; background: rgba(0,0,0,0.02); border: 1px dashed #ccc; border-radius: 12px;">
                    <p style="margin-bottom: 8px; font-weight: 800;">Contact Details</p>
                    <div style="font-size: 14px;">
                        <strong>Phone:</strong> ${app.candidate_phone || 'N/A'} <br>
                        <strong>Email:</strong> ${app.candidate_contact_email || 'N/A'}
                    </div>
                </div>
                
                <div style="margin-top: 16px; font-size: 14px; color: #666;">
                    Status: <strong style="color: ${stColor}">${app.status}</strong> &bull; Match: <strong>${(app.match_score || 0).toFixed(2)}%</strong>
                </div>
            `;
            document.getElementById('candidate-profile-content').innerHTML = html;
        }
