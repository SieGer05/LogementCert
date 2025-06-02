let users = [
   { email: 'test@example.com', password: '123456', name: 'Utilisateur Test', phone: '0123456789' }
];
let currentUser = null;
let listings = [];
let filteredListings = [];
let selectedListing = null;

async function fetchListings() {
   const res = await fetch("http://localhost:8000/public_listings");
   listings = await res.json();
   filteredListings = [...listings];
   renderListings();
}

function showHome() {
   hideAllPages();
   document.getElementById('homePage').classList.add('active');
   renderListings();
}

function showLogin() {
   hideAllPages();
   document.getElementById('loginPage').classList.add('active');
}

function showRegister() {
   hideAllPages();
   document.getElementById('registerPage').classList.add('active');
}

function showBooking(listingId) {
   if (!currentUser) {
      alert('Veuillez vous connecter pour effectuer une réservation.');
      showLogin();
      return;
   }
   selectedListing = listings.find(l => l.id === listingId);
   if (!selectedListing) return;
   hideAllPages();
   document.getElementById('bookingPage').classList.add('active');
   document.getElementById('selectedListing').innerHTML = `
      <div style="display: flex; align-items: center; gap: 1rem;">
         <div style="font-size: 2rem;">${selectedListing.emoji}</div>
         <div>
               <div style="font-weight: bold;">${selectedListing.title}</div>
               <div style="color: #667eea;">${selectedListing.price}</div>
         </div>
      </div>
   `;
   const today = new Date().toISOString().split('T')[0];
   document.getElementById('startDate').min = today;
   document.getElementById('endDate').min = today;
}

function hideAllPages() {
   document.querySelectorAll('.page').forEach(page => {
      page.classList.remove('active');
   });
}

function renderListings(listingsToShow = filteredListings) {
   const grid = document.getElementById('listingsGrid');
   grid.innerHTML = '';
   if (listingsToShow.length === 0) {
      grid.innerHTML = `
         <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: #6b7280;">
               <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
               <h3>Aucun logement trouvé</h3>
               <p>Essayez de modifier vos critères de recherche</p>
         </div>
      `;
      return;
   }
   listingsToShow.forEach(listing => {
      const card = document.createElement('div');
      card.className = 'listing-card';
      let statusText = listing.isBooked ? `Occupé jusqu'au ${formatDate(listing.bookedUntil)}` : 'Disponible';
      let statusClass = listing.isBooked ? 'status-booked' : 'status-available';
      let buttonText = listing.isBooked ? `Réserver à partir du ${formatDate(listing.bookedUntil)}` : 'Louer maintenant';
      let buttonClass = listing.isBooked ? 'booked' : 'available';
      let buttonDisabled = listing.isBooked ? 'disabled' : '';
      let buttonClick = listing.isBooked ? '' : `onclick="showBooking(${listing.id})"`;
      card.innerHTML = `
         <div class="listing-image">${listing.emoji}</div>
         <div class="listing-title">${listing.title}</div>
         <div class="listing-price">${listing.price}</div>
         <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 0.5rem;">
               📍 ${listing.location} • 👥 ${listing.maxGuests} personnes max
         </div>
         <div class="listing-status ${statusClass}">${statusText}</div>
         <button class="rent-btn ${buttonClass}" ${buttonDisabled} ${buttonClick}>
               ${buttonText}
         </button>
      `;
      grid.appendChild(card);
   });
   updateResultsCount(listingsToShow.length);
}

function updateResultsCount(count) {
   const resultsCount = document.getElementById('resultsCount');
   resultsCount.textContent = count === listings.length ? 'Tous les logements' : `${count} logement${count > 1 ? 's' : ''} trouvé${count > 1 ? 's' : ''}`;
}

function performSearch() {
   const searchLocation = document.getElementById('searchLocation').value.toLowerCase();
   const searchCheckin = document.getElementById('searchCheckin').value;
   const searchCheckout = document.getElementById('searchCheckout').value;
   const searchGuests = parseInt(document.getElementById('searchGuests').value);
   filteredListings = listings.filter(listing => {
      if (searchLocation && !listing.location.toLowerCase().includes(searchLocation) && !listing.title.toLowerCase().includes(searchLocation)) {
         return false;
      }
      if (listing.maxGuests < searchGuests) {
         return false;
      }
      if (searchCheckin && searchCheckout) {
         const checkinDate = new Date(searchCheckin);
         const checkoutDate = new Date(searchCheckout);
         if (listing.isBooked && checkinDate <= new Date(listing.bookedUntil)) {
               return false;
         }
      }
      return true;
   });
   applyFilters();
}

function applyFilters() {
   const maxPrice = parseInt(document.getElementById('priceRange').value);
   const availableOnly = document.getElementById('availableOnly').checked;
   const selectedTypes = Array.from(document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked')).map(cb => cb.value);
   let filtered = filteredListings.filter(listing => {
      if (listing.priceValue > maxPrice) {
         return false;
      }
      if (availableOnly && listing.isBooked) {
         return false;
      }
      if (selectedTypes.length > 0 && !selectedTypes.includes(listing.type)) {
         return false;
      }
      return true;
   });
   renderListings(filtered);
}

function sortListings() {
   const sortBy = document.getElementById('sortBy').value;
   const currentListings = [...filteredListings];
   switch (sortBy) {
      case 'price-low':
         currentListings.sort((a, b) => a.priceValue - b.priceValue);
         break;
      case 'price-high':
         currentListings.sort((a, b) => b.priceValue - a.priceValue);
         break;
      case 'name':
         currentListings.sort((a, b) => a.title.localeCompare(b.title));
         break;
   }
   renderListings(currentListings);
}

function updatePriceDisplay() {
   const priceRange = document.getElementById('priceRange');
   const priceDisplay = document.getElementById('priceDisplay');
   priceDisplay.textContent = `${priceRange.value}DH`;
   applyFilters();
}

function formatDate(dateString) {
   return new Date(dateString).toLocaleDateString('fr-FR');
}

function updateAuthUI() {
   const authButtons = document.getElementById('authButtons');
   const userSection = document.getElementById('userSection');
   const welcomeUser = document.getElementById('welcomeUser');
   if (currentUser) {
      authButtons.style.display = 'none';
      userSection.style.display = 'flex';
      userSection.style.alignItems = 'center';
      userSection.style.gap = '1rem';
      welcomeUser.textContent = `Bonjour, ${currentUser.name}`;
   } else {
      authButtons.style.display = 'flex';
      userSection.style.display = 'none';
   }
}

function logout() {
   currentUser = null;
   updateAuthUI();
   showHome();
}

document.getElementById('loginForm').addEventListener('submit', function(e) {
   e.preventDefault();
   const email = document.getElementById('loginEmail').value;
   const password = document.getElementById('loginPassword').value;
   const user = users.find(u => u.email === email && u.password === password);
   if (user) {
      currentUser = user;
      updateAuthUI();
      showHome();
      document.getElementById('loginForm').reset();
   } else {
      alert('Email ou mot de passe incorrect.');
   }
});

document.getElementById('registerForm').addEventListener('submit', function(e) {
   e.preventDefault();
   const name = document.getElementById('registerName').value;
   const email = document.getElementById('registerEmail').value;
   const phone = document.getElementById('registerPhone').value;
   const password = document.getElementById('registerPassword').value;
   const confirmPassword = document.getElementById('confirmPassword').value;
   if (password !== confirmPassword) {
      alert('Les mots de passe ne correspondent pas.');
      return;
   }
   if (users.find(u => u.email === email)) {
      alert('Un compte avec cet email existe déjà.');
      return;
   }
   const newUser = { email, password, name, phone };
   users.push(newUser);
   currentUser = newUser;
   updateAuthUI();
   showHome();
   document.getElementById('registerForm').reset();
   alert('Compte créé avec succès!');
});

document.getElementById('bookingForm').addEventListener('submit', async function(e) {
   e.preventDefault();
   if (!currentUser) {
      document.getElementById('bookingError').textContent = 'Vous devez être connecté pour effectuer une réservation.';
      document.getElementById('bookingError').style.display = 'block';
      return;
   }
   const startDate = document.getElementById('startDate').value;
   const endDate = document.getElementById('endDate').value;
   if (new Date(startDate) >= new Date(endDate)) {
      document.getElementById('bookingError').textContent = 'La date de départ doit être après la date d\'arrivée.';
      document.getElementById('bookingError').style.display = 'block';
      return;
   }
   if (new Date(startDate) < new Date()) {
      document.getElementById('bookingError').textContent = 'La date d\'arrivée ne peut pas être dans le passé.';
      document.getElementById('bookingError').style.display = 'block';
      return;
   }
   const formData = new FormData();
   formData.append("listing_id", selectedListing.id);
   formData.append("user_email", currentUser.email);
   formData.append("user_name", currentUser.name);
   formData.append("start_date", startDate);
   formData.append("end_date", endDate);
   const res = await fetch("http://localhost:8000/book", {
      method: "POST",
      body: formData
   });
   const result = await res.json();
   if (res.ok) {
      selectedListing.isBooked = true;
      selectedListing.bookedUntil = endDate;
      alert('Réservation confirmée! Vous recevrez un email de confirmation.');
      document.getElementById('bookingForm').reset();
      document.getElementById('bookingError').style.display = 'none';
      showHome();
   } else {
      document.getElementById('bookingError').textContent = result.detail || "Erreur lors de la réservation.";
      document.getElementById('bookingError').style.display = 'block';
   }
});

document.getElementById('startDate').addEventListener('change', function() {
   document.getElementById('endDate').min = this.value;
});

document.addEventListener('DOMContentLoaded', function() {
   fetchListings();
   updateAuthUI();
   const today = new Date().toISOString().split('T')[0];
   document.getElementById('searchCheckin').min = today;
   document.getElementById('searchCheckout').min = today;
   document.getElementById('searchLocation').addEventListener('input', performSearch);
   document.getElementById('searchCheckin').addEventListener('change', function() {
      document.getElementById('searchCheckout').min = this.value;
      performSearch();
   });
   document.getElementById('searchCheckout').addEventListener('change', performSearch);
   document.getElementById('searchGuests').addEventListener('change', performSearch);
   document.getElementById('priceRange').addEventListener('input', updatePriceDisplay);
   document.getElementById('availableOnly').addEventListener('change', applyFilters);
   document.querySelectorAll('.checkbox-group input[type="checkbox"]').forEach(cb => {
      cb.addEventListener('change', applyFilters);
   });
   filteredListings = [...listings];
   renderListings();
});