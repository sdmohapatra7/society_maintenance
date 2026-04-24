const Billing = {
    editModal: null,
    init: function() {
        const modalEl = document.getElementById('editBillModal');
        if (modalEl) {
            this.editModal = new bootstrap.Modal(modalEl);
        }
        
        window.markAsPaid = this.markAsPaid.bind(this);
        window.payOnline = this.payOnline.bind(this);
        window.editBill = this.edit.bind(this);
        window.submitEditBill = this.submitEdit.bind(this);
    },

    markAsPaid: function(billId) {
        SocietyPro.confirm('Confirm Payment', 'Are you sure you want to mark this bill as paid manually?', () => {
            SocietyPro.api('/billing/api/' + billId + '/status', 'PUT', {status: 'paid'}, (res) => {
                SocietyPro.alert('Bill marked as paid successfully!', 'success');
                setTimeout(() => location.reload(), 1500);
            });
        });
    },

    payOnline: function(billId) {
        SocietyPro.api('/billing/api/create-order/' + billId, 'POST', {}, (data) => {
            var options = {
                "key": data.key_id,
                "amount": data.amount,
                "currency": "INR",
                "name": "SocietyPro",
                "description": "Maintenance Bill Payment",
                "order_id": data.order_id,
                "handler": (response) => {
                    SocietyPro.api('/billing/api/verify-payment', 'POST', {
                        bill_id: billId,
                        payment_id: response.razorpay_payment_id,
                        order_id: response.razorpay_order_id,
                        signature: response.razorpay_signature
                    }, (verifyRes) => {
                        SocietyPro.alert('Payment successful! Your invoice is updated.', 'success');
                        setTimeout(() => location.reload(), 1500);
                    });
                },
                "theme": { "color": "#8b5cf6" }
            };
            
            if (data.order_id.startsWith('order_mock_')) {
                SocietyPro.confirm('Test Mode', 'This will simulate a successful Razorpay transaction. Continue?', () => {
                    options.handler({
                        razorpay_payment_id: "pay_mock_123",
                        razorpay_order_id: data.order_id,
                        razorpay_signature: "mock_signature"
                    });
                });
                return;
            }

            var rzp = new Razorpay(options);
            rzp.on('payment.failed', function (response){
                SocietyPro.alert("Payment failed: " + response.error.description, 'error');
            });
            rzp.open();
        });
    },

    edit: function(billId) {
        SocietyPro.api('/billing/api/' + billId, 'GET', null, (data) => {
            $('#editBillId').val(data.id);
            let month = data.bill_month;
            if (month && month.length > 7) {
                month = month.substring(0, 7);
            }
            $('#editBillMonth').val(month);
            $('#editAmount').val(data.amount);
            $('#editFixedCharge').val(data.fixed_charge);
            $('#editAreaCharge').val(data.area_charge);
            $('#editDueDate').val(data.due_date);
            $('#editStatus').val(data.status);
            
            this.editModal.show();
        });
    },

    submitEdit: function(e) {
        e.preventDefault();
        if (!SocietyPro.validateForm('#editBillForm')) return;
        
        const id = $('#editBillId').val();
        const data = {
            bill_month: $('#editBillMonth').val() + '-01',
            amount: parseFloat($('#editAmount').val()),
            fixed_charge: parseFloat($('#editFixedCharge').val()),
            area_charge: parseFloat($('#editAreaCharge').val()),
            due_date: $('#editDueDate').val(),
            status: $('#editStatus').val()
        };
        
        SocietyPro.api('/billing/api/' + id, 'PUT', data, (res) => {
            this.editModal.hide();
            SocietyPro.alert('Bill updated successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        });
    }
};

$(document).ready(() => Billing.init());
