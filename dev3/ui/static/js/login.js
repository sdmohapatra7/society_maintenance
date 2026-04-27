function togglePassword() {
    const $pwd = $('#password');
    const $icon = $('#toggleIcon');
    if ($pwd.attr('type') === 'password') {
        $pwd.attr('type', 'text');
        $icon.removeClass('fa-eye').addClass('fa-eye-slash');
    } else {
        $pwd.attr('type', 'password');
        $icon.removeClass('fa-eye-slash').addClass('fa-eye');
    }
}

$(document).ready(() => {
    // Any other login initialization logic
});
