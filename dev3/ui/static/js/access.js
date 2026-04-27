const Access = {
    updateRoleAccess: function(role, featureName, canAccess) {
        SocietyPro.api('/access/update', 'POST', {
            role: role,
            feature_name: featureName,
            can_access: canAccess
        }, function(res) {
            console.log('Role access updated');
        });
    }
};

$(document).ready(() => {
    window.updateRoleAccess = Access.updateRoleAccess.bind(Access);
});
