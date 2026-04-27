const Events = {
    submit: function() {
        if (!SocietyPro.validateForm('#addEventForm')) return;
        
        const data = {
            title: $('input[name="title"]').val(),
            event_date: $('input[name="event_date"]').val(),
            location: $('input[name="location"]').val(),
            description: $('textarea[name="description"]').val()
        };
        
        SocietyPro.api('/events/add', 'POST', data, () => {
            SocietyPro.alert("Event created successfully!", "success");
            setTimeout(() => location.reload(), 800);
        });
    },

    openEditModal: function(id, title, date, location, description) {
        $('#eventId').val(id);
        $('input[name="title"]').val(title);
        $('input[name="event_date"]').val(date);
        $('input[name="location"]').val(location);
        $('textarea[name="description"]').val(description);
        
        $('.modal-title').text('Edit Event');
        $('#addEventModal .btn-primary').text('Save Changes').attr('onclick', 'Events.update()');
        
        const modal = new bootstrap.Modal(document.getElementById('addEventModal'));
        modal.show();
    },

    update: function() {
        if (!SocietyPro.validateForm('#addEventForm')) return;
        
        const id = $('#eventId').val();
        const data = {
            title: $('input[name="title"]').val(),
            event_date: $('input[name="event_date"]').val(),
            location: $('input[name="location"]').val(),
            description: $('textarea[name="description"]').val()
        };
        
        SocietyPro.api(`/events/edit/${id}`, 'POST', data, () => {
            SocietyPro.alert("Event updated successfully!", "success");
            setTimeout(() => location.reload(), 800);
        });
    },

    delete: function(id) {
        SocietyPro.confirm('Delete Event', 'Are you sure you want to delete this event?', () => {
            SocietyPro.api(`/events/delete/${id}`, 'POST', {}, () => location.reload());
        });
    }
};

$(document).ready(() => {
    $('#addEventModal').on('hidden.bs.modal', function () {
        $('#eventId').val('');
        $('#addEventForm')[0].reset();
        $('.modal-title').text('Create Event');
        $('#addEventModal .btn-primary').text('Create').attr('onclick', 'Events.submit()');
        $('#addEventForm').removeClass('was-validated');
    });
});
