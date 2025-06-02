const API_BASE_URL = "http://localhost:8000";

function logout() {
   alert("Déconnexion réussie.");
   window.location.href = "login.html";
}

document.getElementById('propertyForm').addEventListener('submit', async e => {
   e.preventDefault();
   const formData = new FormData(e.target);
   formData.append("owner", "owner");
   const res = await fetch(`${API_BASE_URL}/blockchain/submit_property`, {
      method: "POST",
      body: formData
   });
   const result = await res.json();
   if (res.ok) {
      alert(result.message);
      e.target.reset();
      loadMyProperties();
   } else {
      alert("Erreur: " + result.detail);
   }
});

async function loadMyProperties() {
   const res = await fetch(`${API_BASE_URL}/blockchain/properties?owner=owner`);
   const data = await res.json();
   const tbody = document.getElementById("ownerProperties");
   tbody.innerHTML = "";
   data.forEach(entry => {
      const tx = entry.transaction;
      const row = document.createElement("tr");
      row.innerHTML = `
         <td>${tx.title}</td>
         <td>${tx.status}</td>
         <td>🧾</td>
      `;
      tbody.appendChild(row);
   });
}

document.addEventListener('DOMContentLoaded', loadMyProperties);