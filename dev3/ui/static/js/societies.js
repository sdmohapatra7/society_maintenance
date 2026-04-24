const Societies = {
    modal: null,
    editingId: null,
    init: function() {
        this.modal = new bootstrap.Modal($('#societyModal')[0]);
        this.loadGrid();
        $('#societyForm').on('submit', this.handleFormSubmit.bind(this));
        
        window.editSociety = this.edit.bind(this);
        window.deleteSociety = this.delete.bind(this);
    },

    loadGrid: function() {
        SocietyPro.api('/societies/api', 'GET', null, (data) => {
            const columns = [
                { key: 'id', label: 'ID' },
                { key: 'name', label: 'Name', format: (v, row) => `<a href="/houses/society/${row.id}" class="text-decoration-none fw-bold">${v}</a>` },
                { key: 'registration_no', label: 'Reg No' },
                { key: 'contact_email', label: 'Email' }
            ];

            const actions = [
                { label: 'Edit', icon: 'fa-edit', class: 'btn-outline-primary', onClick: 'editSociety' },
                { label: 'Delete', icon: 'fa-trash', class: 'btn-outline-danger', onClick: 'deleteSociety' }
            ];

            SocietyPro.renderTable('#societiesGrid', columns, data, actions);
        });
    },

    handleFormSubmit: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#societyForm')) return;
        
        const method = this.editingId ? 'PUT' : 'POST';
        const url = this.editingId ? `/societies/api/${this.editingId}` : '/societies/api';
        
        const data = {};
        $(e.target).serializeArray().forEach(item => data[item.name] = item.value);

        SocietyPro.api(url, method, data, (res) => {
            this.loadGrid();
            this.modal.hide();
            SocietyPro.alert(this.editingId ? 'Society updated successfully' : 'Society created successfully', 'success');
            this.resetForm();
        });
    },

    edit: function(id) {
        SocietyPro.api('/societies/api', 'GET', null, (data) => {
            const item = data.find(d => d.id === id);
            if (item) {
                this.editingId = id;
                ['name', 'address', 'registration_no', 'contact_email'].forEach(key => {
                    $(`[name="${key}"]`).val(item[key]);
                });
                $('.modal-title').text('Edit Society');
                this.modal.show();
            }
        });
    },

    delete: function(id) {
        SocietyPro.confirm('Delete Society', 'Are you sure you want to delete this society and all its data?', () => {
            SocietyPro.api(`/societies/api/${id}`, 'DELETE', null, () => {
                SocietyPro.alert('Society deleted successfully', 'success');
                this.loadGrid();
            });
        });
    },

    resetForm: function() {
        this.editingId = null;
        $('#societyForm')[0].reset();
        $('#societyForm').removeClass('was-validated');
        $('.modal-title').text('Add Society');
    }
};

$(document).ready(() => Societies.init());
