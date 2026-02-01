if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            hashed_password = generate_password_hash('admin123')
            admin = User(username='admin', password=hashed_password)
            db.session.add(admin)
            db.session.commit()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
