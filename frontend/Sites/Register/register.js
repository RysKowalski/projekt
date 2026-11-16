import { API } from "/api.js";

const form = document.getElementById("formBox");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username == "" || password == "") {
    document.getElementById("errorMessage").innerHTML = "Nie podano wszystkich danych";
    return;
  }

  try {
    const response = await fetch("/api/register", {
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

    if (response.status == 200) {
      await API.login(username, password)
      console.log(await API.get("/api/me"))
    }
  }

  catch (error) {
    console.error("Błąd połączenia z serwerem: ", error);
  }
});
