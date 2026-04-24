const Houses = {
    modal: null,
    billModal: null,
    editingId: null,
    societyId: null,
    
    init: function() {
        this.modal = new bootstrap.Modal($('#houseModal')[0]);
        this.billModal = new bootstrap.Modal($('#billModal')[0]);
        this.societyId = $('#societyId').val();
        
        this.loadGrid();
        $('#houseForm').on('submit', this.handleFormSubmit.bind(this));
        $('#billForm').on('submit', this.handleGenerateBill.bind(this));

        window.editHouse = this.edit.bind(this);
        window.deleteHouse = this.delete.bind(this);
        window.openBillModal = this.openBillDialog.bind(this);
    },

    loadGrid: function() {
        SocietyPro.api(`/houses/api/society/${this.societyId}`, 'GET', null, (data) => {
            const columns = [
                { key: 'wing', label: 'Wing' },
                { key: 'house_no', label: 'House No' },
                { key: 'house_type', label: 'Type' },
                { key: 'area_sq_ft', label: 'Area' },
                { key: 'resident_name', label: 'Resident' }
            ];

            const actions = [
                { label: 'Bill', icon: 'fa-file-invoice', class: 'btn-outline-success', onClick: 'openBillModal' },
                { label: 'Edit', icon: 'fa-edit', class: 'btn-outline-primary', onClick: 'editHouse' },
                { label: 'Delete', icon: 'fa-trash', class: 'btn-outline-danger', onClick: 'deleteHouse' }
            ];

            SocietyPro.renderTable('#housesGrid', columns, data, actions);
        });
    },

    handleFormSubmit: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#houseForm')) return;

        const method = this.editingId ? 'PUT' : 'POST';
        const url = this.editingId ? `/houses/api/${this.editingId}` : '/houses/api';
        
        const data = { society_id: this.societyId };
        $(e.target).serializeArray().forEach(item => data[item.name] = item.value);

        SocietyPro.api(url, method, data, (res) => {
            this.loadGrid();
            this.modal.hide();
            SocietyPro.alert(this.editingId ? 'House updated successfully' : 'House created successfully. Welcome email sent!', 'success');
            this.resetForm();
        });
    },

    edit: function(id) {
        SocietyPro.api(`/houses/api/society/${this.societyId}`, 'GET', null, (data) => {
            const item = data.find(d => d.id === id);
            if (item) {
                this.editingId = id;
                ['wing', 'house_no', 'area_sq_ft', 'house_type', 'resident_name', 'resident_email', 'resident_phone'].forEach(key => {
                    $(`[name="${key}"]`).val(item[key]);
                });
                $('.modal-title').text('Edit House');
                this.modal.show();
            }
        });
    },

    delete: function(id) {
        SocietyPro.confirm('Delete House', 'Are you sure you want to delete this house record?', () => {
            SocietyPro.api(`/houses/api/${id}`, 'DELETE', null, () => {
                SocietyPro.alert('House deleted successfully', 'success');
                this.loadGrid();
            });
        });
    },

    openBillDialog: function(id) {
        SocietyPro.api(`/houses/api/society/${this.societyId}`, 'GET', null, (data) => {
            const item = data.find(d => d.id === id);
            if (item) {
                $('#billHouseId').val(id);
                $('#billTarget').text(`${item.wing}-${item.house_no} (${item.resident_name})`);
                // Storing area in a data attribute or hidden input for the calc
                $('#billModal').data('area', item.area_sq_ft);
                this.billModal.show();
            }
        });
    },

    handleGenerateBill: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#billForm')) return;
        
        const houseId = $('#billHouseId').val();
        const area = $('#billModal').data('area');
        const fixed = parseFloat($('[name="fixed_charge"]').val());
        const rate = parseFloat($('[name="area_rate"]').val());
        const amount = fixed + (area * rate);

        const data = {
            house_id: houseId,
            bill_month: $('[name="bill_month"]').val(),
            fixed_charge: fixed,
            area_charge: area * rate,
            amount: amount,
            due_date: $('[name="due_date"]').val()
        };

        SocietyPro.api('/billing/generate', 'POST', data, (res) => {
            this.billModal.hide();
            SocietyPro.alert('Maintenance bill generated and sent to resident!', 'success');
        });
    },

    resetForm: function() {
        this.editingId = null;
        $('#houseForm')[0].reset();
        $('#houseForm').removeClass('was-validated');
        $('.modal-title').text('Add House');
    }
};

$(document).ready(() => Houses.init());
