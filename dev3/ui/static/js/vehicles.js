const Vehicles = {
    submit: function() {
        if (!SocietyPro.validateForm('#addVehicleForm')) return;
        
        const data = {
            license_plate: $('input[name="license_plate"]').val().toUpperCase(),
            make_model: $('input[name="make_model"]').val(),
            vehicle_type: $('select[name="vehicle_type"]').val(),
            house_id: $('select[name="house_id"]').val(),
            parking_slot: $('input[name="parking_slot"]').val()
        };
        
        SocietyPro.api('/vehicles/add', 'POST', data, () => {
            SocietyPro.alert("Vehicle registered successfully!", "success");
            setTimeout(() => location.reload(), 800);
        });
    },

    openEditModal: function(id, license, make, type, houseId, slot) {
        $('#vehicleId').val(id);
        $('input[name="license_plate"]').val(license);
        $('input[name="make_model"]').val(make);
        $('select[name="vehicle_type"]').val(type);
        $('select[name="house_id"]').val(houseId);
        $('input[name="parking_slot"]').val(slot);
        
        $('.modal-title').text('Edit Vehicle');
        $('#addVehicleModal .btn-primary').text('Save Changes').attr('onclick', 'Vehicles.update()');
        
        const modal = new bootstrap.Modal(document.getElementById('addVehicleModal'));
        modal.show();
    },

    update: function() {
        if (!SocietyPro.validateForm('#addVehicleForm')) return;
        
        const id = $('#vehicleId').val();
        const data = {
            license_plate: $('input[name="license_plate"]').val().toUpperCase(),
            make_model: $('input[name="make_model"]').val(),
            vehicle_type: $('select[name="vehicle_type"]').val(),
            house_id: $('select[name="house_id"]').val(),
            parking_slot: $('input[name="parking_slot"]').val()
        };
        
        SocietyPro.api(`/vehicles/edit/${id}`, 'POST', data, () => {
            SocietyPro.alert("Vehicle updated successfully!", "success");
            setTimeout(() => location.reload(), 800);
        });
    },

    delete: function(id) {
        SocietyPro.confirm('Remove Vehicle', 'Are you sure you want to remove this vehicle record?', () => {
            SocietyPro.api(`/vehicles/delete/${id}`, 'POST', {}, () => {
                SocietyPro.alert("Vehicle removed successfully!", "success");
                setTimeout(() => location.reload(), 800);
            });
        });
    }
};

$(document).ready(() => {
    $('#addVehicleModal').on('hidden.bs.modal', function () {
        $('#vehicleId').val('');
        $('#addVehicleForm')[0].reset();
        $('.modal-title').text('Register Vehicle');
        $('#addVehicleModal .btn-primary').text('Register').attr('onclick', 'Vehicles.submit()');
        $('#addVehicleForm').removeClass('was-validated');
    });
});
