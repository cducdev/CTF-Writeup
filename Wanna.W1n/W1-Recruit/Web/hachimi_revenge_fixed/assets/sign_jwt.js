const { readFileSync } = require("fs");
const jwt = require("jsonwebtoken");
const sshpk = require("sshpk");

const PUBLIC_KEY_PATH = "../secrets/key.pub";

function parseKey(key) {
	const parsedKey = sshpk.parseKey(key, "ssh", { filename: "publickey" });
	return parsedKey.toString("ssh");
}

const publicRaw = readFileSync(PUBLIC_KEY_PATH, "utf8");

const secret = parseKey(publicRaw);

const payload = {
	sub: "1",
	username: "admin",
};

const token = jwt.sign(payload, secret);
console.log(token);
