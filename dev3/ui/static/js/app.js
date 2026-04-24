const SocietyPro = {
    init: function() {
        console.log("SocietyPro Initialized");
        this.handleLoader();
        this.initValidation();
        this.confirmModal = new bootstrap.Modal($('#confirmModal')[0]);
        this.toast = new bootstrap.Toast($('#liveToast')[0]);
    },

    alert: function(message, type = 'primary') {
        const $toast = $('#liveToast');
        const $msg = $('#toastMessage');
        $msg.text(message);
        
        $toast.attr('class', 'toast border-0 shadow-lg align-items-center text-white bg-' + type);
        this.toast.show();
    },

    confirm: function(title, message, onConfirm) {
        $('#confirmTitle').text(title);
        $('#confirmMessage').text(message);
        const $confirmBtn = $('#confirmBtn');
        
        // Remove old listeners to avoid multiple calls using jQuery's off()
        $confirmBtn.off('click').on('click', () => {
            this.confirmModal.hide();
            onConfirm();
        });
        
        this.confirmModal.show();
    },

    initValidation: function() {
        $('.needs-validation').each(function() {
            $(this).on('submit', function(event) {
                if (!this.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                $(this).addClass('was-validated');
            });
        });
    },

    handleLoader: function() {
        $(window).on('load', function() {
            $('#loader').fadeOut('slow');
        });
    },

    ajax: function(url, method, data, success, error) {
        let options = {
            url: url,
            method: method,
            success: success,
            error: (err) => {
                const msg = err.responseJSON?.error || 'Something went wrong';
                if (error) error(err);
                else this.alert(msg, 'danger');
            }
        };

        if (data instanceof FormData) {
            options.processData = false;
            options.contentType = false;
            options.data = data;
        } else {
            options.contentType = 'application/json';
            options.data = JSON.stringify(data);
        }

        return $.ajax(options);
    },

    api: function(url, method, data, callback) {
        return this.ajax(url, method, data, callback);
    },

    validateForm: function(formSelector) {
        const $form = $(formSelector);
        if ($form[0].checkValidity() === false) {
            $form.addClass('was-validated');
            return false;
        }
        return true;
    },

    renderTable: function(targetSelector, columns, data, actions = []) {
        const $container = $(targetSelector);
        if (!data || data.length === 0) {
            $container.html('<div class="text-center p-5 text-muted"><i class="fas fa-folder-open mb-3 d-block" style="font-size: 3rem; opacity: 0.3;"></i><p>No records found</p></div>');
            return;
        }

        let html = '<div class="table-responsive"><table class="table table-hover align-middle"><thead><tr>';
        columns.forEach(col => html += `<th>${col.label}</th>`);
        html += '<th class="text-end">Actions</th></tr></thead><tbody>';

        data.forEach(row => {
            html += '<tr>';
            columns.forEach(col => {
                let val = row[col.key] || '';
                if (col.format) val = col.format(val, row);
                html += `<td>${val}</td>`;
            });
            
            html += '<td class="text-end">';
            actions.forEach(action => {
                const icon = action.icon || 'fa-question';
                const cls = action.class || 'btn-outline-primary';
                html += `<button class="btn btn-sm ${cls} ms-1" title="${action.label}" onclick="${action.onClick}(${row.id})"><i class="fas ${icon}"></i></button>`;
            });
            html += '</td></tr>';
        });

        html += '</tbody></table></div>';
        $container.html(html);
    }
};

$(document).ready(() => SocietyPro.init());