async function postAnalyze(formData) {
  const resp = await fetch('/analyze', { method: 'POST', body: formData });
  return resp.json();
}

function riskClass(label) {
  if (!label) return '';
  const l = label.toLowerCase();
  if (l.includes('safe') || l.includes('low')) return 'risk-safe';
  if (l.includes('moderate') || l.includes('medium')) return 'risk-moderate';
  return 'risk-high';
}

function renderReport(data) {
  const reportDiv = document.getElementById('report');
  reportDiv.innerHTML = '';

  // Support both single-analysis and multiple-drug responses
  const analyses = data.drug_analyses || (Array.isArray(data) ? data : [data]);

  analyses.forEach(drug => {
    const risk = drug.risk_assessment || drug.risk || {};
    const profile = drug.pharmacogenomic_profile || {};
    const cls = riskClass(risk.risk_label || risk.label || risk);

    reportDiv.innerHTML += `
      <div class="card ${cls}">
        <h2>${drug.drug || ''}</h2>
        <p><b>Risk:</b> ${risk.risk_label || risk.label || 'N/A'}</p>
        <p><b>Severity:</b> ${risk.severity || 'N/A'}</p>
        <p><b>Gene:</b> ${profile.primary_gene || 'N/A'}</p>
        <p><b>Phenotype:</b> ${profile.phenotype || 'N/A'}</p>
        <hr/>
      </div>
    `;
  });
}

document.getElementById('analyze').addEventListener('click', async () => {
  const status = document.getElementById('status');
  const patientId = document.getElementById('patient_id').value || '';
  const drug = document.getElementById('drug_select').value;
  const fileInput = document.getElementById('vcf_file');

  if (!fileInput.files.length) {
    status.innerText = 'Please choose a VCF file.';
    return;
  }

  const fd = new FormData();
  fd.append('patient_id', patientId);
  fd.append('drug', drug);
  fd.append('vcf_file', fileInput.files[0]);

  status.innerText = 'Analyzing...';
  try {
    const data = await postAnalyze(fd);
    status.innerText = '';
    renderReport(data);
  } catch (e) {
    status.innerText = 'Analysis failed: ' + e.message;
  }
});
