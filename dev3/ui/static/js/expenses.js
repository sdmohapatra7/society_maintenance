const Expenses = {
    modal: null,
    init: function() {
        this.modal = new bootstrap.Modal($('#expenseModal')[0]);
        $('#expenseForm').on('submit', this.handleSubmit.bind(this));
    },

    handleSubmit: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#expenseForm')) return;
        
        const id = $('#expenseId').val();
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/expenses/api/${id}` : '/expenses/api';
        
        const formData = new FormData($('#expenseForm')[0]);
        
        // Client-side file validation
        const fileInput = $('input[name="receipt"]')[0];
        if (fileInput && fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const ext = file.name.split('.').pop().toLowerCase();
            const allowed = ['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'];
            if (!allowed.includes(ext)) {
                SocietyPro.alert('Invalid file format. Allowed: PDF, Images, DOCX', 'danger');
                return;
            }
        }
        
        // Use raw AJAX for FormData
        $.ajax({
            url: url,
            type: method,
            data: formData,
            processData: false,
            contentType: false,
            success: (res) => {
                SocietyPro.alert(id ? "Expense updated!" : "Expense recorded!", "success");
                setTimeout(() => location.reload(), 800);
            },
            error: (err) => {
                SocietyPro.alert("Error saving expense", "error");
            }
        });
    },

    edit: function(id) {
        SocietyPro.api(`/expenses/api/${id}`, 'GET', null, (data) => {
            $('#expenseId').val(data.id);
            $('input[name="title"]').val(data.title);
            $('input[name="amount"]').val(data.amount);
            $('input[name="expense_date"]').val(data.expense_date);
            $('select[name="category"]').val(data.category);
            $('textarea[name="description"]').val(data.description);
            
            $('.modal-title').text('Edit Expense');
            this.modal.show();
        });
    },

    delete: function(id) {
        SocietyPro.confirm('Delete Expense', 'Are you sure you want to delete this expense record?', () => {
            SocietyPro.api(`/expenses/api/${id}`, 'DELETE', null, () => {
                SocietyPro.alert("Expense deleted!", "success");
                setTimeout(() => location.reload(), 800);
            });
        });
    }
};

$(document).ready(() => {
    Expenses.init();
    
    $('#expenseModal').on('hidden.bs.modal', function() {
        $('#expenseId').val('');
        $('#expenseForm')[0].reset();
        $('.modal-title').text('Record New Expense');
        $('#expenseForm').removeClass('was-validated');
    });
});
