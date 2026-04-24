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
    }
};

$(document).ready(() => {
    window.updateSetting = Settings.updateSetting.bind(Settings);
    window.addMaster = Settings.addMaster.bind(Settings);
    window.deleteMaster = Settings.deleteMaster.bind(Settings);
});
