let logSource = null;

function formatSalary(inputId, labelId) {
    const val = parseInt(document.getElementById(inputId).value);
    const el = document.getElementById(labelId);
    if (!val || isNaN(val)) { el.textContent = ''; return; }
    const formatted = '₹ ' + new Intl.NumberFormat('en-IN').format(val);
    let label = '';
    if (val >= 10000000) {
        const cr = val / 10000000;
        label = ` (${cr % 1 === 0 ? cr : cr.toFixed(2)}Cr)`;
    } else if (val >= 100000) {
        const lakhs = val / 100000;
        label = ` (${lakhs % 1 === 0 ? lakhs : lakhs.toFixed(1)}L)`;
    }
    el.textContent = formatted + label;
}
function openTab(event, tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(tabId).style.display = 'block';
    if(event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }
}

// Load Config from Backend
async function loadConfig() {
    try {
        const resp = await fetch('/api/config');
        if (!resp.ok) return;
        const data = await resp.json();
        
        document.getElementById('search-terms').value = (data.search_terms || []).join(', ');
        document.getElementById('location').value = data.search_location || '';
        document.getElementById('first-name').value = data.first_name || '';
        document.getElementById('last-name').value = data.last_name || '';
        document.getElementById('phone-number').value = data.phone_number || '';
        document.getElementById('desired-salary').value = data.desired_salary || '';
        document.getElementById('current-ctc').value = data.current_ctc || '';
        formatSalary('desired-salary', 'desired-salary-fmt');
        formatSalary('current-ctc', 'current-ctc-fmt');
        document.getElementById('notice-period').value = data.notice_period || '';
        document.getElementById('linkedin-url').value = data.linkedin_url || '';
        document.getElementById('years-of-experience').value = data.years_of_experience || '';
        
        // Populate checkboxes
        const checkGroup = (name, values) => {
            const arr = values || [];
            document.querySelectorAll(`input[type="checkbox"][name="${name}"]`).forEach(cb => {
                cb.checked = arr.includes(cb.value);
            });
        };
        
        // Populate radios
        const radioGroup = (name, value) => {
            if (!value) return;
            const cb = document.querySelector(`input[type="radio"][name="${name}"][value="${value}"]`);
            if (cb) cb.checked = true;
        };
        
        checkGroup('experience', data.experience_level);
        checkGroup('job-type', data.job_type);
        checkGroup('onsite', data.on_site);
        
        radioGroup('sort-by', data.sort_by);
        radioGroup('date-posted', data.date_posted);

        const compGrid = document.getElementById('company-grid');
        compGrid.innerHTML = '';
        (data.companies || []).forEach(comp => addCompanyToUI(comp, true));
        
        document.getElementById('easy-apply').checked = !!data.easy_apply_only;
        
        const skillsContainer = document.getElementById('skills-list-container');
        skillsContainer.innerHTML = '';
        if(data.skills) {
            Object.entries(data.skills).forEach(([skill, exp]) => addSkillToUI(skill, exp));
        }
    } catch (err) {
        console.error('Failed to load config:', err);
    }
}

function addSkillToUI(skillName, yearsExp) {
    if (!skillName.trim()) return;
    const container = document.getElementById('skills-list-container');
    const div = document.createElement('div');
    div.className = 'skill-item';
    div.style.cssText = 'display:flex; justify-content:space-between; padding:0.5rem; background:var(--bg-hover); border-radius:4px;';
    div.innerHTML = `
        <span><strong>${skillName}</strong> (${yearsExp} years)</span>
        <button onclick="this.parentElement.remove()" style="background:none; border:none; color:red; cursor:pointer;">Remove</button>
    `;
    div.dataset.skill = skillName;
    div.dataset.exp = yearsExp;
    container.appendChild(div);
}

document.getElementById('btn-add-skill').addEventListener('click', () => {
    const nameInput = document.getElementById('add-skill-name');
    const expInput = document.getElementById('add-skill-exp');
    if (!nameInput.value || !expInput.value) return;
    addSkillToUI(nameInput.value, parseInt(expInput.value));
    nameInput.value = '';
    expInput.value = '1';
});

function addCompanyToUI(companyName, isChecked = true) {
    if (!companyName.trim()) return;
    const grid = document.getElementById('company-grid');
    // Check if exists
    if (document.querySelector(`input[name="company-item"][value="${companyName.replace(/"/g, '&quot;')}"]`)) return;
    
    const lbl = document.createElement('label');
    lbl.style.display = 'flex';
    lbl.style.alignItems = 'center';
    lbl.style.gap = '0.4rem';
    lbl.style.fontSize = '0.85rem';
    lbl.innerHTML = `<input type="checkbox" name="company-item" value="${companyName.replace(/"/g, '&quot;')}" ${isChecked ? 'checked' : ''}> ${companyName}`;
    grid.appendChild(lbl);
}

document.getElementById('btn-add-company').addEventListener('click', () => {
    const input = document.getElementById('add-company-input');
    addCompanyToUI(input.value);
    input.value = '';
});

// Resume Upload Handler
document.getElementById('resume-upload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const nameLabel = document.getElementById('resume-file-name');
    nameLabel.textContent = `Uploading ${file.name}...`;
    nameLabel.style.color = 'var(--text-color)';
    
    const formData = new FormData();
    formData.append('resume', file);
    
    try {
        const resp = await fetch('/api/upload-resume', { method: 'POST', body: formData });
        if (resp.ok) {
            nameLabel.textContent = `${file.name} uploaded successfully!`;
            nameLabel.style.color = 'var(--color-success)';
        } else {
            throw new Error('Upload failed');
        }
    } catch (error) {
        nameLabel.textContent = `Failed to upload ${file.name}`;
        nameLabel.style.color = 'var(--color-danger)';
    }
});

// Save Config
document.getElementById('btn-save-config').addEventListener('click', async () => {
    const btn = document.getElementById('btn-save-config');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i data-lucide="loader" class="spin"></i> Saving...';
    lucide.createIcons();
    
    const getChecked = (name) => {
        return Array.from(document.querySelectorAll(`input[type="checkbox"][name="${name}"]:checked`)).map(cb => cb.value);
    };
    
    const getRadio = (name) => {
        const checked = document.querySelector(`input[type="radio"][name="${name}"]:checked`);
        return checked ? checked.value : "";
    };

    const getSkills = () => {
        const skills = {};
        document.querySelectorAll('#skills-list-container .skill-item').forEach(el => {
            skills[el.dataset.skill] = parseInt(el.dataset.exp);
        });
        return skills;
    };

    const payload = {
        search_terms: document.getElementById('search-terms').value.split(',').map(s => s.trim()).filter(s => s),
        search_location: document.getElementById('location').value.trim(),
        experience_level: getChecked('experience'),
        job_type: getChecked('job-type'),
        on_site: getChecked('onsite'),
        sort_by: getRadio('sort-by'),
        date_posted: getRadio('date-posted'),
        companies: getChecked('company-item'),
        easy_apply_only: document.getElementById('easy-apply').checked,
        
        first_name: document.getElementById('first-name').value.trim(),
        last_name: document.getElementById('last-name').value.trim(),
        phone_number: document.getElementById('phone-number').value.trim(),
        desired_salary: parseInt(document.getElementById('desired-salary').value) || 0,
        current_ctc: parseInt(document.getElementById('current-ctc').value) || 0,
        notice_period: parseInt(document.getElementById('notice-period').value) || 0,
        linkedin_url: document.getElementById('linkedin-url').value.trim(),
        years_of_experience: document.getElementById('years-of-experience').value.trim(),
        skills: getSkills()
    };
    
    try {
        const resp = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (resp.ok) {
            btn.innerHTML = '<i data-lucide="check"></i> Saved!';
            lucide.createIcons();
            setTimeout(() => { btn.innerHTML = originalText; lucide.createIcons(); }, 2000);
        } else {
            throw new Error('Save failed');
        }
    } catch (err) {
        btn.innerHTML = '<i data-lucide="x"></i> Error';
        lucide.createIcons();
        setTimeout(() => { btn.innerHTML = originalText; lucide.createIcons(); }, 2000);
    }
});

// Appending Log Lines
function appendLog(msg, type = '') {
    const term = document.getElementById('terminal-window');
    const div = document.createElement('div');
    div.className = `terminal-line ${type}`;
    div.textContent = msg;
    term.appendChild(div);
    term.scrollTop = term.scrollHeight;
}

// Terminal Connection
function connectTerminal() {
    if (logSource) logSource.close();
    
    logSource = new EventSource('/api/logs');
    logSource.onmessage = (event) => {
        if (event.data === 'STREAM_DONE') {
            appendLog('--- Bot Finished / Stopped ---', 'system');
            document.getElementById('btn-start-bot').style.display = 'inline-flex';
            document.getElementById('btn-stop-bot').style.display = 'none';
            logSource.close();
        } else {
            const txt = event.data;
            let type = '';
            if (txt.toLowerCase().includes('error') || txt.toLowerCase().includes('failed')) type = 'error';
            else if (txt.toLowerCase().includes('success') || txt.toLowerCase().includes('applied to')) type = 'success';
            appendLog(txt, type);
        }
    };
    logSource.onerror = () => { logSource.close(); };
}

// Start Bot Action
document.getElementById('btn-start-bot').addEventListener('click', async () => {
    try {
        const resp = await fetch('/api/start', { method: 'POST' });
        if (resp.ok) {
            document.getElementById('terminal-window').innerHTML = '';
            appendLog('--- Bot Started ---', 'system');
            document.getElementById('btn-start-bot').style.display = 'none';
            document.getElementById('btn-stop-bot').style.display = 'inline-flex';
            connectTerminal();
        }
    } catch(err) {
        appendLog(`Failed to start: ${err}`, 'error');
    }
});

// Stop Bot Action
document.getElementById('btn-stop-bot').addEventListener('click', async () => {
    try {
        await fetch('/api/stop', { method: 'POST' });
        appendLog('Stopping bot...', 'system');
    } catch(err) {
        console.error(err);
    }
});

document.getElementById('btn-clear-terminal').addEventListener('click', () => {
    document.getElementById('terminal-window').innerHTML = '';
});

// Jobs History Table Loader
async function loadJobs() {
    try {
        const resp = await fetch('/applied-jobs');
        if (!resp.ok) return;
        const jobs = await resp.json();
        const tbody = document.getElementById('jobsBody');
        tbody.innerHTML = '';
        jobs.forEach((job, index) => {
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><a href="${job.Job_Link}" target="_blank">${job.Title}</a></td>
                <td>${job.Company}</td>
                <td>${job.HR_Name && job.HR_Name !== 'Unknown' ? `<a href="${job.HR_Link}" target="_blank">${job.HR_Name}</a>` : 'N/A'}</td>
                <td>${job.External_Job_link === 'Easy Applied' ? 'Easy Applied' : (job.External_Job_link && job.External_Job_link !== 'nan' ? `<a href="${job.External_Job_link}" target="_blank">External Link</a>` : 'N/A')}</td>
                <td>${job.Date_Applied !== 'Pending' ? '<span class="tick">✓</span> ' + job.Date_Applied.split(' ')[0] : 'Pending'}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error('Failed to load jobs table:', err);
    }
}

// Initial Initialization
lucide.createIcons();
loadConfig();
loadJobs();
