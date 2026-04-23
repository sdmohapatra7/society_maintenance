const Expenses = {
    modal: null,
    init: function() {
        this.modal = new bootstrap.Modal(document.getElementById('expenseModal'));
        $('#expenseForm').on('submit', this.handleCreate.bind(this));
    },

    handleCreate: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#expenseForm')) return;

        const formData = new FormData(e.target);
        SocietyPro.api('/expenses/api', 'POST', formData, (res) => {
            location.reload();
        });
    }
};

$(document).ready(() => Expenses.init());
