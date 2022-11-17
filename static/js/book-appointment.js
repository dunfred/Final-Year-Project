const bookAppointmentElm = document.getElementById('book-appointment-modal');
const bookCtaElm = document.getElementById('book-cta');
const closeModalElm = document.getElementById('close-modal');


console.log(bookAppointmentElm);
console.log(bookCtaElm);

bookCtaElm.addEventListener('click', showModal);
closeModalElm.addEventListener('click', hideModal);

function showModal() {
    bookAppointmentElm.style.display = 'block';
}

function hideModal() {
    bookAppointmentElm.style.display = 'none';
}