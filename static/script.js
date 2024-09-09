ddocument.getElementById("deployButton").addEventListener("click", async () => {
    try {
        let response = await fetch("/deploy_contract", { method: "POST" });
        let data = await response.json();
        document.getElementById("deployResult").textContent = "Transaction ID: " + data.transaction_id;
    } catch (error) {
        document.getElementById("deployResult").textContent = "Error deploying contract: " + error.message;
    }
});

document.getElementById("voteButton").addEventListener("click", async () => {
    try {
        let voterAddress = document.getElementById("voterAddress").value;
        let candidateId = document.getElementById("candidateId").value;
        let response = await fetch("/vote", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ voter_address: voterAddress, candidate_id: candidateId })
        });
        let data = await response.json();
        document.getElementById("voteResult").textContent = "Transaction ID: " + data.transaction_id;
    } catch (error) {
        document.getElementById("voteResult").textContent = "Error voting: " + error.message;
    }
});

document.getElementById("resultsButton").addEventListener("click", async () => {
    try {
        let response = await fetch("/results");
        let data = await response.json();
        document.getElementById("results").textContent = JSON.stringify(data.results, null, 2);
    } catch (error) {
        document.getElementById("results").textContent = "Error fetching results: " + error.message;
    }
});

document.getElementById("accountButton").addEventListener("click", async () => {
    try {
        let address = document.getElementById("accountAddress").value;
        let response = await fetch(`/account/${address}`);
        let data = await response.json();
        document.getElementById("accountInfo").textContent = JSON.stringify(data.account_info, null, 2);
    } catch (error) {
        document.getElementById("accountInfo").textContent = "Error fetching account.html info: " + error.message;
    }
});
