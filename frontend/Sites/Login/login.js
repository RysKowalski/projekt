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

  await API.login(username, password)

  console.log(await API.get("/api/me", {}))
});
