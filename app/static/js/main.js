document.addEventListener('DOMContentLoaded', () => {
    const cvFile = document.getElementById('cvFile');
    const fileName = document.getElementById('fileName');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const jobDesc = document.getElementById('jobDesc');
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('resultsSection');

    // File input change handler
    cvFile.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileName.textContent = e.target.files[0].name;
            fileName.style.color = '#333';
            fileName.style.fontWeight = 'bold';
        }
    });

    // Analyze button click handler
    analyzeBtn.addEventListener('click', async () => {
        if (!cvFile.files[0] || !jobDesc.value.trim()) {
            alert('Veuillez uploader un CV et fournir une description de poste.');
            return;
        }

        const formData = new FormData();
        formData.append('cv', cvFile.files[0]);
        formData.append('job_desc', jobDesc.value);

        loading.style.display = 'flex';
        resultsSection.style.display = 'none';

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Erreur lors de l\'analyse');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Une erreur est survenue. Veuillez réessayer.');
        } finally {
            loading.style.display = 'none';
        }
    });

    function displayResults(data) {
        resultsSection.style.display = 'block';
        
        // Inject HTML structure if not present (since index.html has empty resultsSection)
        if (!document.getElementById('totalScore')) {
            resultsSection.innerHTML = `
                <div class="card results-header">
                    <h2>Résultats de l'Analyse</h2>
                    <div class="scores-grid">
                        <div class="score-card">
                            <div class="score-circle" id="totalScoreCircle">
                                <span id="totalScore">0%</span>
                            </div>
                            <label>Score Global</label>
                        </div>
                        <div class="score-card">
                            <div class="score-circle small" id="skillScoreCircle">
                                <span id="skillScore">0%</span>
                            </div>
                            <label>Compétences</label>
                        </div>
                        <div class="score-card">
                            <div class="score-circle small" id="semanticScoreCircle">
                                <span id="semanticScore">0%</span>
                            </div>
                            <label>Expérience</label>
                        </div>
                        <div class="score-card">
                            <div class="score-circle small" id="educationScoreCircle">
                                <span id="educationScore">0%</span>
                            </div>
                            <label>Formation</label>
                        </div>
                    </div>
                </div>

                <div class="details-grid">
                    <div class="card">
                        <h3>✅ Points Forts</h3>
                        <div id="matchingSkills" class="tags-container"></div>
                    </div>
                    <div class="card">
                        <h3>⚠️ Compétences Manquantes</h3>
                        <div id="missingSkills" class="tags-container"></div>
                    </div>
                </div>

                <div class="card">
                    <h3>ℹ️ Informations Extraites</h3>
                    <div class="info-row">
                        <strong>Emails:</strong> <span id="extractedEmails">-</span>
                    </div>
                    <div class="info-row">
                        <strong>Compétences CV:</strong> <span id="cvSkillsCount">-</span>
                    </div>
                    <div class="info-row">
                        <strong>Compétences Requises:</strong> <span id="jobSkillsCount">-</span>
                    </div>
                </div>
            `;
        }

        // Update Scores
        updateScore('totalScore', 'totalScoreCircle', data.total_score);
        updateScore('skillScore', 'skillScoreCircle', data.skill_score);
        updateScore('semanticScore', 'semanticScoreCircle', data.text_similarity);
        updateScore('educationScore', 'educationScoreCircle', data.education_score);

        // Update Skills
        const matchingContainer = document.getElementById('matchingSkills');
        const missingContainer = document.getElementById('missingSkills');
        
        matchingContainer.innerHTML = '';
        missingContainer.innerHTML = '';

        if (data.matching_skills.length === 0) {
            matchingContainer.innerHTML = '<span class="text-muted">Aucune compétence directe trouvée.</span>';
        } else {
            data.matching_skills.forEach(skill => {
                const tag = document.createElement('span');
                tag.className = 'tag match';
                tag.textContent = skill;
                matchingContainer.appendChild(tag);
            });
        }

        if (data.missing_skills.length === 0) {
            missingContainer.innerHTML = '<span class="text-success">Toutes les compétences requises sont présentes !</span>';
        } else {
            data.missing_skills.forEach(skill => {
                const tag = document.createElement('span');
                tag.className = 'tag missing';
                tag.textContent = skill;
                missingContainer.appendChild(tag);
            });
        }

        // Update Info
        document.getElementById('extractedEmails').textContent = data.emails.length > 0 ? data.emails.join(', ') : 'Aucun email détecté';
        document.getElementById('cvSkillsCount').textContent = data.cv_skills_count;
        document.getElementById('jobSkillsCount').textContent = data.job_skills_count;
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function updateScore(textId, circleId, score) {
        const textEl = document.getElementById(textId);
        const circleEl = document.getElementById(circleId);
        
        // Animate number
        let current = 0;
        const timer = setInterval(() => {
            current += 1;
            textEl.textContent = current + '%';
            if (current >= score) clearInterval(timer);
        }, 10);

        // Update circle gradient
        circleEl.style.background = `conic-gradient(#4CAF50 ${score * 3.6}deg, #eee 0deg)`;
    }
});
