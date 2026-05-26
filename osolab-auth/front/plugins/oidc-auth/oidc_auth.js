(function () {
  "use strict";

  var module = angular.module("taigaContrib.oidcAuth", []);

  function joinUrl() {
    var parts = Array.prototype.slice.call(arguments)
      .filter(function (part) {
        return part !== null && part !== undefined && part !== "";
      })
      .map(function (part) {
        return String(part);
      });

    if (!parts.length) {
      return "";
    }

    return parts
      .map(function (part, index) {
        if (index === 0) {
          return part.replace(/\/+$/, "");
        }
        return part.replace(/^\/+|\/+$/g, "");
      })
      .join("/");
  }

  function OIDCLoginButtonDirective(
    $window,
    $params,
    $location,
    $config,
    $events,
    $confirm,
    $auth,
    $navUrls,
    $loader,
    $rootScope
  ) {
    function link($scope, $el) {
      function scrubLoginParams() {
        [
          "accepted_terms",
          "auth_token",
          "big_photo",
          "bio",
          "color",
          "date_joined",
          "email",
          "full_name",
          "full_name_display",
          "gravatar_id",
          "id",
          "is_active",
          "lang",
          "max_memberships_private_projects",
          "max_memberships_public_projects",
          "max_private_projects",
          "max_public_projects",
          "next",
          "photo",
          "read_new_terms",
          "refresh",
          "roles",
          "theme",
          "timezone",
          "total_private_projects",
          "total_public_projects",
          "type",
          "username",
          "uuid",
          "verified_email"
        ].forEach(function (name) {
          $location.search(name, null);
        });
      }

      function loginSuccess() {
        $auth.removeToken();
        var data = _.clone($params, false);
        var user = $auth.model.make_model("users", data);

        $auth.setToken(user.auth_token);
        $auth.setUser(user);
        $rootScope.$broadcast("auth:login", user);
        $events.setupConnection();

        var nextUrl =
          $params.next && $params.next !== $navUrls.resolve("login")
            ? $params.next
            : $navUrls.resolve("home");

        scrubLoginParams();
        $location.path(nextUrl);
      }

      function loginError() {
        var errorDescription = $params.error_description;

        $location.search("type", null);
        $location.search("error", null);
        $location.search("error_description", null);

        $confirm.notify(
          "light-error",
          errorDescription || "Could not complete OIDC login."
        );
      }

      function loginWithOIDCAccount() {
        if ($params.type !== "oidc") {
          return;
        }

        if ($params.error) {
          loginError();
        } else {
          loginSuccess();
        }
      }

      loginWithOIDCAccount();

      $el.on("click", ".button-auth", function (event) {
        event.preventDefault();

        var nextUrl =
          $params.next && $params.next !== $navUrls.resolve("login")
            ? $params.next
            : $navUrls.resolve("home");
        var baseUrl = $config.get("api", "/api/v1/").split("/").slice(0, -3).join("/");
        var url = joinUrl(baseUrl, $config.get("oidcMountPoint", "/oidc"), "authenticate/");

        $window.location.href = url + "?next=" + encodeURIComponent(nextUrl);
      });

      $scope.$on("$destroy", function () {
        $el.off();
      });

      $scope.buttonText = $config.get("oidcButtonText", "OpenID Connect");
      $scope.buttonImage = $config.get("oidcButtonImage", "logo.gif");
    }

    return {
      link: link,
      restrict: "EA",
      template: ""
    };
  }

  module.directive("tgOidcLoginButton", [
    "$window",
    "$routeParams",
    "$tgLocation",
    "$tgConfig",
    "$tgEvents",
    "$tgConfirm",
    "$tgAuth",
    "$tgNavUrls",
    "tgLoader",
    "$rootScope",
    OIDCLoginButtonDirective
  ]);
})();
