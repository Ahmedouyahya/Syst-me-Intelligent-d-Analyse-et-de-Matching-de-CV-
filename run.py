from app import create_app, db
from app.models import User, Company, Candidate, JobOffer, Application

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Company': Company, 'Candidate': Candidate, 'JobOffer': JobOffer, 'Application': Application}

if __name__ == '__main__':
    app.run(debug=True)
