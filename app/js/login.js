document.getElementById('loginForm').addEventListener('submit', async function(e) {
   e.preventDefault();
   const formData = new FormData(this);
   const res = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      body: formData
   });
   const result = await res.json();
   const resultDiv = document.getElementById('loginResult');
   if (res.ok && result.role === "authority") {
      resultDiv.innerHTML = '<p style="color:green;">Connexion autorité réussie. Redirection...</p>';
      setTimeout(() => window.location.href = 'authoritypanel.html', 1000);
   } else if (res.ok && result.role === "owner") {
      resultDiv.innerHTML = '<p style="color:green;">Connexion propriétaire réussie. Redirection...</p>';
      setTimeout(() => window.location.href = 'ownerdashboard.html', 1000);
   } else {
      resultDiv.innerHTML = `<p style="color:red;">${result.detail}</p>`;
   }
});