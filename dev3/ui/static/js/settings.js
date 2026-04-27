const Settings = {
    updateSetting: function(key) {
        const value = $(`#set_${key}`).val();
        SocietyPro.api('/settings/app/update', 'POST', { key, value }, () => {
            SocietyPro.alert('Setting updated successfully!', 'success');
        });
    },

    addMaster: function(category, index) {
        const label = $(`#new_label_${index}`).val();
        const value = $(`#new_value_${index}`).val();
        if(!label || !value) return SocietyPro.alert('Please fill both fields', 'error');

        SocietyPro.api('/settings/master/add', 'POST', { category, label, value }, () => {
            location.reload();
        });
    },

    deleteMaster: function(id) {
        SocietyPro.confirm('Delete Master Entry', 'Are you sure?', () => {
            SocietyPro.api(`/settings/master/delete/${id}`, 'DELETE', null, () => {
                location.reload();
            });
        });
    },

    submitRole: function() {
        const data = {
            name: $('#addRoleForm input[name="name"]').val(),
            description: $('#addRoleForm textarea[name="description"]').val()
        };
        if(!data.name) return SocietyPro.alert('Role Name is required', 'error');

        SocietyPro.api('/settings/role/add', 'POST', data, (res) => {
            if(res.success) {
                SocietyPro.alert('Role created successfully!', 'success');
                setTimeout(() => location.reload(), 800);
            } else {
                SocietyPro.alert('Error: ' + res.error, 'error');
            }
        });
    },

    deleteRole: function(id) {
        SocietyPro.confirm('Delete Role', 'Are you sure you want to delete this role?', () => {
            SocietyPro.api(`/settings/role/delete/${id}`, 'DELETE', null, () => {
                SocietyPro.alert('Role deleted', 'success');
                setTimeout(() => location.reload(), 800);
            });
        });
    }
};

$(document).ready(() => {
    window.updateSetting = Settings.updateSetting.bind(Settings);
    window.addMaster = Settings.addMaster.bind(Settings);
    window.deleteMaster = Settings.deleteMaster.bind(Settings);
    window.submitRole = Settings.submitRole.bind(Settings);
    window.deleteRole = Settings.deleteRole.bind(Settings);
});
