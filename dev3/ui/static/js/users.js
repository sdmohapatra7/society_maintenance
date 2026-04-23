const Users = {
    modal: null,
    editingId: null,
    init: function() {
        this.modal = new bootstrap.Modal(document.getElementById('userModal'));
        this.loadGrid();
        $('#userForm').on('submit', this.handleFormSubmit.bind(this));
        
        window.deleteUser = this.delete.bind(this);
        window.editUser = this.edit.bind(this);
    },

    loadGrid: function() {
        SocietyPro.api('/users/api', 'GET', null, (data) => {
            const columns = [
                { key: 'id', label: 'ID' },
                { key: 'username', label: 'Username' },
                { key: 'email', label: 'Email' },
                { key: 'role', label: 'Role', format: (v) => `<span class="badge bg-info text-dark">${v}</span>` }
            ];

            const actions = [
                { label: 'Edit', icon: 'fa-edit', class: 'btn-outline-primary', onClick: 'editUser' },
                { label: 'Delete', icon: 'fa-trash', class: 'btn-outline-danger', onClick: 'deleteUser' }
            ];

            SocietyPro.renderTable('#usersGrid', columns, data, actions);
        });
    },

    handleFormSubmit: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#userForm')) return;
        
        const method = this.editingId ? 'PUT' : 'POST';
        const url = this.editingId ? `/users/api/${this.editingId}` : '/users/api';
        
        const data = {};
        $(e.target).serializeArray().forEach(item => data[item.name] = item.value);

        SocietyPro.api(url, method, data, (res) => {
            this.loadGrid();
            this.modal.hide();
            this.resetForm();
        });
    },

    edit: function(id) {
        SocietyPro.api('/users/api', 'GET', null, (data) => {
            const item = data.find(d => d.id === id);
            if (item) {
                this.editingId = id;
                $('input[name="username"]').val(item.username).prop('disabled', true);
                $('input[name="email"]').val(item.email);
                $('input[name="password"]').val('').prop('required', false);
                $('select[name="role"]').val(item.role);
                $('.modal-title').text('Edit User');
                this.modal.show();
            }
        });
    },

    delete: function(id) {
        if (confirm('Are you sure you want to delete this user?')) {
            SocietyPro.api(`/users/api/${id}`, 'DELETE', null, () => this.loadGrid());
        }
    },

    resetForm: function() {
        this.editingId = null;
        $('#userForm')[0].reset();
        $('#userForm').removeClass('was-validated');
        $('input[name="username"]').prop('disabled', false);
        $('input[name="password"]').prop('required', true);
        $('.modal-title').text('Create New User');
    }
};

$(document).ready(() => Users.init());
