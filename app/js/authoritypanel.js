function logout() {
   alert("Déconnexion réussie.");
   window.location.href = "login.html";
}

document.getElementById('verificationForm').addEventListener('submit', async e => {
   e.preventDefault();
   const fileInput = document.getElementById('keyFile');
   const file = fileInput.files[0];
   const result = document.getElementById('verificationResult');
   if (!file) {
      result.innerHTML = "<p style='color:red;'>Aucun fichier sélectionné.</p>";
      return;
   }
   const reader = new FileReader();
   reader.onload = async function(event) {
      const fileContent = event.target.result;
      result.innerHTML = `
         <div class="card">
               <p><strong>Clé lue :</strong></p>
               <pre style="white-space:pre-wrap;">${fileContent}</pre>
         </div>
      `;
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch("http://localhost:8000/validator/add", {
         method: "POST",
         body: formData
      });
      const json = await res.json();
      result.innerHTML += `<p style="color:green;"><strong>${json.message}</strong></p>`;
   };
   reader.onerror = function() {
      result.innerHTML = "<p style='color:red;'>Erreur lors de la lecture du fichier.</p>";
   };
   reader.readAsText(file);
});

async function loadStats() {
   const res = await fetch("http://localhost:8000/stats");
   const stats = await res.json();
   document.getElementById("blockchainStats").innerHTML = `
      <p><strong>Blocs totaux :</strong> ${stats.total_blocks}</p>
      <p><strong>Transactions validées :</strong> ${stats.validated_transactions}</p>
   `;
}

async function loadPendingValidations() {
   const res = await fetch("http://localhost:8000/pending");
   const list = await res.json();
   const container = document.getElementById("pendingValidations");
   container.innerHTML = "";
   list.forEach(tx => {
      const card = document.createElement("div");
      card.classList.add("card");
      card.innerHTML = `
         <p><strong>${tx.title || 'Sans titre'}</strong></p>
         <p>${tx.description || 'Pas de description'}</p>
         <p><strong>${tx.price || '?'} DH</strong></p>
      `;
      const approveBtn = document.createElement("button");
      approveBtn.textContent = "Approuver";
      approveBtn.onclick = () => approveTransaction(tx.title);
      card.appendChild(approveBtn);
      container.appendChild(card);
   });
}

async function approveTransaction(title) {
   const privateKey = prompt("Entrez la clé privée PEM pour signer le bloc :");
   const formData = new FormData();
   formData.append("private_key", privateKey);
   formData.append("title", title);
   const res = await fetch("http://localhost:8000/mine", {
      method: "POST",
      body: formData
   });
   const result = await res.json();
   alert(result.message);
   loadStats();
   loadPendingValidations();
}

document.addEventListener('DOMContentLoaded', () => {
   loadStats();
   loadPendingValidations();
});