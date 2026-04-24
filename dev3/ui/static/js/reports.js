const Reports = {
    modal: null,
    init: function() {
        this.modal = new bootstrap.Modal($('#reportModal')[0]);
        
        window.openReportModal = this.open.bind(this);
        window.setFY = this.setFY.bind(this);
    },

    open: function(type) {
        $('#reportType').val(type);
        $('#reportModalTitle').text((type === 'billing' ? 'Billing' : 'Expense') + ' Report Configuration');
        
        // Toggle status filter visibility
        if (type === 'billing') {
            $('#statusFilter').show();
        } else {
            $('#statusFilter').hide();
        }
        
        this.modal.show();
    },

    setFY: function(start, end) {
        $('input[name="from_date"]').val(start);
        $('input[name="to_date"]').val(end);
    }
};

$(document).ready(() => Reports.init());
