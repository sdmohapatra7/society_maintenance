const Complaints = {
    modal: null,
    editingId: null,
    init: function() {
        this.modal = new bootstrap.Modal(document.getElementById('complaintModal'));
        this.loadGrid();
        $('#complaintForm').on('submit', this.handleFormSubmit.bind(this));
        
        // Expose to window for inline onclicks in renderTable
        window.resolveComplaint = this.resolve.bind(this);
        window.deleteComplaint = this.delete.bind(this);
        window.editComplaint = this.edit.bind(this);
    },

    loadGrid: function() {
        SocietyPro.api('/complaints/api', 'GET', null, (data) => {
            const columns = [
                { key: 'id', label: 'ID' },
                { key: 'title', label: 'Title' },
                { key: 'status', label: 'Status', format: (v) => {
                    const cls = v === 'open' ? 'bg-warning text-dark' : 'bg-success';
                    return `<span class="badge ${cls}">${v}</span>`;
                }},
            ];
            
            if (data.length > 0 && data[0].username) {
                columns.push({ key: 'username', label: 'Reported By' });
            }

            const actions = [
                { label: 'Edit', icon: 'fa-edit', class: 'btn-outline-primary', onClick: 'editComplaint' },
                { label: 'Delete', icon: 'fa-trash', class: 'btn-outline-danger', onClick: 'deleteComplaint' }
            ];

            // Add Resolve only if it's open and user has rights (handled by backend but UI should match)
            // For now let's just show it.
            actions.unshift({ label: 'Resolve', icon: 'fa-check', class: 'btn-outline-success', onClick: 'resolveComplaint' });

            SocietyPro.renderTable('#complaintsGrid', columns, data, actions);
        });
    },

    handleFormSubmit: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#complaintForm')) return;
        
        const method = this.editingId ? 'PUT' : 'POST';
        const url = this.editingId ? `/complaints/api/${this.editingId}` : '/complaints/api';
        
        let data;
        if (this.editingId) {
            data = {
                title: $('input[name="title"]').val(),
                description: $('textarea[name="description"]').val()
            };
        } else {
            data = new FormData(e.target);
        }

        SocietyPro.api(url, method, data, (res) => {
            this.loadGrid();
            this.modal.hide();
            this.resetForm();
        });
    },

    edit: function(id) {
        // Fetch fresh data or use existing if small
        SocietyPro.api('/complaints/api', 'GET', null, (data) => {
            const item = data.find(d => d.id === id);
            if (item) {
                this.editingId = id;
                $('input[name="title"]').val(item.title);
                $('textarea[name="description"]').val(item.description);
                $('.modal-title').text('Edit Complaint');
                this.modal.show();
            }
        });
    },

    delete: function(id) {
        if (confirm('Are you sure you want to delete this complaint?')) {
            SocietyPro.api(`/complaints/api/${id}`, 'DELETE', null, () => this.loadGrid());
        }
    },

    resolve: function(id) {
        if(confirm('Mark this complaint as resolved?')) {
            SocietyPro.api(`/complaints/api/${id}/status`, 'PATCH', { status: 'resolved' }, () => this.loadGrid());
        }
    },

    resetForm: function() {
        this.editingId = null;
        $('#complaintForm')[0].reset();
        $('#complaintForm').removeClass('was-validated');
        $('.modal-title').text('File a Complaint');
    }
};

$(document).ready(() => Complaints.init());
