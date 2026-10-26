const form = document.getElementById("formBox");

form.addEventListener("submit", async(event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://83.229.84.40:2532/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "*/*",
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });

        console.log(response.status);
        console.log(await response.text());
    }

    catch (error) {
        console.error("Błąd połączenia z serwerem: ", error);
    }
});