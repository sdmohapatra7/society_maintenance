const Visitors = {
    submit: function() {
        if (!SocietyPro.validateForm('#addVisitorForm')) return;
        
        const data = {
            name: $('input[name="name"]').val(),
            phone: $('input[name="phone"]').val(),
            purpose: $('select[name="purpose"]').val(),
            house_id: $('select[name="house_id"]').val()
        };
        
        SocietyPro.api('/visitors/add', 'POST', data, () => {
            SocietyPro.alert("Visitor logged successfully!", "success");
            setTimeout(() => location.reload(), 800);
        });
    },

    openEditModal: function(id, name, phone, purpose, houseId) {
        $('#visitorId').val(id);
        $('input[name="name"]').val(name);
        $('input[name="phone"]').val(phone);
        $('select[name="purpose"]').val(purpose);
        $('select[name="house_id"]').val(houseId);
        
        $('.modal-title').text('Edit Visitor Log');
        $('#addVisitorModal .btn-primary').text('Save Changes').attr('onclick', 'Visitors.update()');
        
        const modal = new bootstrap.Modal(document.getElementById('addVisitorModal'));
        modal.show();
    },

    update: function() {
        if (!SocietyPro.validateForm('#addVisitorForm')) return;
        
        const id = $('#visitorId').val();
        const data = {
            name: $('input[name="name"]').val(),
            phone: $('input[name="phone"]').val(),
            purpose: $('select[name="purpose"]').val(),
            house_id: $('select[name="house_id"]').val()
        };
        
        SocietyPro.api(`/visitors/edit/${id}`, 'POST', data, () => {
            SocietyPro.alert("Visitor updated successfully!", "success");
            setTimeout(() => location.reload(), 800);
        });
    },

    checkout: function(id) {
        SocietyPro.confirm('Checkout Visitor', 'Mark visitor as checked out?', () => {
            SocietyPro.api(`/visitors/checkout/${id}`, 'POST', {}, () => {
                SocietyPro.alert("Visitor checked out!", "success");
                setTimeout(() => location.reload(), 800);
            });
        });
    },

    delete: function(id) {
        SocietyPro.confirm('Delete Log', 'Are you sure you want to delete this visitor log permanently?', () => {
            SocietyPro.api(`/visitors/delete/${id}`, 'POST', {}, () => {
                SocietyPro.alert("Visitor log deleted!", "success");
                setTimeout(() => location.reload(), 800);
            });
        });
    }
};

$(document).ready(() => {
    $('#addVisitorModal').on('hidden.bs.modal', function () {
        $('#visitorId').val('');
        $('#addVisitorForm')[0].reset();
        $('.modal-title').text('Log Visitor Entry');
        $('#addVisitorModal .btn-primary').text('Log Entry').attr('onclick', 'Visitors.submit()');
        $('#addVisitorForm').removeClass('was-validated');
    });
});
