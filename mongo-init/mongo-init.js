db = db.getSiblingDB('windForecaster');

db.createUser({
    user: "__MONGO_APP_USER__",
    pwd: "__MONGO_APP_PASSWORD__",
    roles: [{
        role: "readWrite",
        db: "windForecaster"
    }]
});
