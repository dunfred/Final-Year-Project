const isStudentElm      = document.getElementById('is_student');
const studentContainer  = document.getElementById('student-form-container');
const workerContainer   = document.getElementById('worker-form-container');

// #Student fields
const reg_numberElm     = document.getElementById('registration_number');
const programmeElm      = document.getElementById('programme');
const departmentElm     = document.getElementById('department');
const levelElm          = document.getElementById('level');
const residenceElm      = document.getElementById('residence');
const home_phoneElm     = document.getElementById('home_phone');

// #Worker fields
const workerElm         = document.getElementById('worker');
const work_typeElm      = document.getElementById('work_type');
const organizationElm   = document.getElementById('organization');


isStudentElm.addEventListener('change', updateForm);

function updateForm() {
    if (isStudentElm.value.toLocaleLowerCase() == "yes") {
        studentContainer.style.display = 'block';
        workerContainer.style.display = 'none';
        workerElm.value = 'no';
        
        // Make these fields required
        reg_numberElm.setAttribute('required', '');
        programmeElm.setAttribute('required', '');
        departmentElm.setAttribute('required', '');
        levelElm.setAttribute('required', '');
        residenceElm.setAttribute('required', '');
        home_phoneElm.setAttribute('required', '');

        // Make these fields not required
        workerElm.removeAttribute('required');
        work_typeElm.removeAttribute('required');
        organizationElm.removeAttribute('required');

    }
    else if (isStudentElm.value.toLocaleLowerCase() == "no") {
        studentContainer.style.display = 'none';
        workerContainer.style.display = 'block';
        workerElm.value = 'yes';

        // Make these fields required
        workerElm.setAttribute('required', '');
        work_typeElm.setAttribute('required', '');
        organizationElm.setAttribute('required', '');
        
        // Make these fields not required
        reg_numberElm.removeAttribute('required');
        programmeElm.removeAttribute('required');
        departmentElm.removeAttribute('required');
        levelElm.removeAttribute('required');
        residenceElm.removeAttribute('required');
        home_phoneElm.removeAttribute('required');
    }
    else {
        studentContainer.style.display = 'block';
        workerContainer.style.display = 'block';
        workerElm.value = 'no';

        // Make these fields not required
        reg_numberElm.removeAttribute('required');
        programmeElm.removeAttribute('required');
        departmentElm.removeAttribute('required');
        levelElm.removeAttribute('required');
        residenceElm.removeAttribute('required');
        home_phoneElm.removeAttribute('required');
        workerElm.removeAttribute('required');
        work_typeElm.removeAttribute('required');
        organizationElm.removeAttribute('required');
    }
}