// Google Rank Tracker Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const rankForm = document.getElementById('rankForm');
    const checkBtn = document.getElementById('checkBtn');
    const uploadBtn = document.getElementById('uploadBtn');
    const csvFile = document.getElementById('csvFile');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContainer = document.getElementById('resultsContainer');
    const loadHistoryBtn = document.getElementById('loadHistoryBtn');
    const historyContainer = document.getElementById('historyContainer');

    // Handle form submission
    rankForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const websiteUrl = document.getElementById('websiteUrl').value.trim();
        const keywordsText = document.getElementById('keywords').value.trim();
        const location = document.getElementById('location').value;
        
        if (!websiteUrl || !keywordsText) {
            showError('Please fill in all required fields');
            return;
        }
        
        // Parse keywords (one per line)
        const keywords = keywordsText.split('\n')
            .map(k => k.trim())
            .filter(k => k.length > 0);
        
        if (keywords.length === 0) {
            showError('Please enter at least one keyword');
            return;
        }
        
        // Disable button and show loading
        checkBtn.disabled = true;
        checkBtn.querySelector('.btn-text').style.display = 'none';
        checkBtn.querySelector('.btn-loader').style.display = 'inline';
        
        try {
            const response = await fetch('/api/check-rankings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    website_url: websiteUrl,
                    keywords: keywords,
                    location: location
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'An error occurred');
            }
            
            // Display results
            displayResults(data.results, websiteUrl, location, data.saved);
            
        } catch (error) {
            showError(error.message);
        } finally {
            // Re-enable button
            checkBtn.disabled = false;
            checkBtn.querySelector('.btn-text').style.display = 'inline';
            checkBtn.querySelector('.btn-loader').style.display = 'none';
        }
    });
    
    // Handle CSV upload
    uploadBtn.addEventListener('click', function() {
        csvFile.click();
    });
    
    csvFile.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('file', file);
        
        uploadBtn.disabled = true;
        uploadBtn.textContent = '⏳ Uploading...';
        
        try {
            const response = await fetch('/api/upload-keywords', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }
            
            // Fill keywords textarea
            document.getElementById('keywords').value = data.keywords.join('\n');
            showSuccess(`Loaded ${data.count} keywords from CSV file`);
            
        } catch (error) {
            showError(error.message);
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.textContent = '📁 Upload CSV';
            csvFile.value = '';
        }
    });
    
    // Handle history loading
    loadHistoryBtn.addEventListener('click', async function() {
        const websiteUrl = document.getElementById('historyUrl').value.trim();
        const keyword = document.getElementById('historyKeyword').value.trim();
        
        loadHistoryBtn.disabled = true;
        loadHistoryBtn.textContent = '⏳ Loading...';
        historyContainer.innerHTML = '<div class="loading">Loading history</div>';
        
        try {
            const params = new URLSearchParams();
            if (websiteUrl) params.append('website_url', websiteUrl);
            if (keyword) params.append('keyword', keyword);
            params.append('limit', '50');
            
            const response = await fetch(`/api/history?${params.toString()}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to load history');
            }
            
            displayHistory(data.results);
            
        } catch (error) {
            historyContainer.innerHTML = `<div class="error-message">${error.message}</div>`;
        } finally {
            loadHistoryBtn.disabled = false;
            loadHistoryBtn.textContent = 'Load History';
        }
    });
    
    // Display results
    function displayResults(results, websiteUrl, location, saved) {
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
        let html = '';
        
        if (saved) {
            html += '<div class="success-message">✅ Results saved successfully!</div>';
        }
        
        html += '<div class="results-grid">';
        
        results.forEach(result => {
            const statusClass = result.status;
            const positionText = result.status === 'not_found' ? '> 100' : result.position;
            const statusIcon = result.status === 'success' ? '✅' : 
                             result.status === 'not_found' ? '⚠️' : '❌';
            
            html += `
                <div class="result-item ${statusClass}">
                    <div class="result-header">
                        <div class="result-keyword">${statusIcon} ${escapeHtml(result.keyword)}</div>
                        <div class="result-position">${positionText}</div>
                    </div>
                    <div class="result-details">
                        ${result.found_url ? `<a href="${escapeHtml(result.found_url)}" target="_blank">${escapeHtml(result.found_url)}</a><br>` : ''}
                        ${result.serp_title ? `<strong>${escapeHtml(result.serp_title)}</strong><br>` : ''}
                        ${result.serp_snippet ? `<span>${escapeHtml(result.serp_snippet)}</span><br>` : ''}
                        <small>Checked on: ${escapeHtml(result.checked_on)}</small>
                        ${result.error ? `<br><span style="color: #dc3545;">Error: ${escapeHtml(result.error)}</span>` : ''}
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        resultsContainer.innerHTML = html;
    }
    
    // Display history
    function displayHistory(results) {
        if (results.length === 0) {
            historyContainer.innerHTML = '<div class="error-message">No history found</div>';
            return;
        }
        
        let html = '<div class="results-grid">';
        
        results.forEach(result => {
            const positionText = result.status === 'not_found' ? '> 100' : result.position;
            const statusIcon = result.status === 'success' ? '✅' : 
                             result.status === 'not_found' ? '⚠️' : '❌';
            
            html += `
                <div class="history-item">
                    <div class="history-info">
                        <div class="history-keyword">${statusIcon} ${escapeHtml(result.keyword)}</div>
                        <div class="history-url">${escapeHtml(result.website_url)}</div>
                        <small>${escapeHtml(result.checked_on)}</small>
                    </div>
                    <div class="history-position">${positionText}</div>
                </div>
            `;
        });
        
        html += '</div>';
        historyContainer.innerHTML = html;
    }
    
    // Show error message
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        // Insert at top of form
        rankForm.insertBefore(errorDiv, rankForm.firstChild);
        
        // Remove after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    // Show success message
    function showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = message;
        
        // Insert at top of form
        rankForm.insertBefore(successDiv, rankForm.firstChild);
        
        // Remove after 3 seconds
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }
    
    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});




