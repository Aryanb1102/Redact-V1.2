document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsDiv = document.getElementById('results');
    const serviceListDiv = document.getElementById('service-list');
    const loadingImg = document.getElementById('loading');
    const emailForm = document.getElementById('email-form');
    const emailTemplate = document.getElementById('email-template');
    const contactEmailP = document.getElementById('contact-email');
  
    let allResults = [];
  
    searchForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      serviceListDiv.innerHTML = '';
      resultsDiv.classList.add('hidden');
      loadingImg.classList.remove('hidden');
  
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
  
      const resp = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email })
      });
      loadingImg.classList.add('hidden');
      const data = await resp.json();
  
      if (data.results && data.results.length > 0) {
        allResults = data.results;
        resultsDiv.classList.remove('hidden');
        allResults.forEach(service => {
          const div = document.createElement('div');
          div.classList.add('service');
          div.innerHTML = `
            <strong>Website:</strong> ${service.website}<br>
            <strong>URL:</strong> ${service.url && service.url !== 'N/A' ? `<a href="${service.url}" target="_blank">${service.url}</a>` : 'N/A'}<br>
            <strong>Deletion Possible:</strong> ${service.deletion_possible ? 'Yes' : 'No'}<br>
            <strong>Manual Steps:</strong> ${service.manual_steps}<br>
            <strong>Contact Method:</strong> ${service.contact_method}
          `;
          serviceListDiv.appendChild(div);
        });
      } else {
        resultsDiv.classList.remove('hidden');
        serviceListDiv.innerHTML = 'No results found or your data not found.';
      }
    });
  
    emailForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const website = document.getElementById('website').value;
      const name = document.getElementById('user-name').value;
      const userEmail = document.getElementById('user-email').value;
  
      const resp = await fetch('/generate-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ website, name, email: userEmail })
      });
      const data = await resp.json();
      if (data.email_template) {
        emailTemplate.value = data.email_template;
        contactEmailP.textContent = data.contact_email ? `Send this email to: ${data.contact_email}` : '';
      } else {
        emailTemplate.value = data.error || 'Error generating template';
        contactEmailP.textContent = '';
      }
    });
  });
  