(function (ng) {
	'use strict';

	// dummy service to fulfill dependency if Google reCaptcha is deactivated
	ng.module('vcRecaptcha').service('vcRecaptchaService', function() {
		this.getResponse = function() {
			return null;
		};
	});
});
