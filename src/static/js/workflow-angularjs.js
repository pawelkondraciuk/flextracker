angular.module('workflow', ['workflow.urls'])
    .config(['$httpProvider', function($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ])
    .controller('WorkflowController', ['$scope', '$window', 'TemplateData', 'WorkflowFactory', function ($scope, $window, TemplateData, WorkflowFactory) {

        $scope.workflow = undefined;
        $scope.loading = true;
        var id = TemplateData.id;

        $scope.addStatus = function() {
            WorkflowFactory.createStatus({
                name: 'Status',
                type: 2
            }).success(function(result) {
                $scope.workflow.states.push(result)
            }).error(function(result) {
                alert(result);
            })
        };

        $scope.removeStatus = function(idx) {
            $scope.workflow.states.splice(idx, 1);
        };

        $scope.send = function() {
            angular.forEach($scope.workflow.states, function(state) {
                var _state = angular.copy(state);
                for (var i = 0; i < state.available_states.length; i++) {
                    state.available_states[i] = Number(state.available_states[i]);
                }
            })
            if (id == undefined) {
                if (TemplateData.projectId == undefined) {
                    $window.opener.workflow({id: $scope.workflow.id, value: $scope.workflow.name});
                    $window.close();
                    return;
                }
                WorkflowFactory.bind($scope.workflow, TemplateData.projectId)
                    .success(function (result) {
                        $window.opener.workflow({id: $scope.workflow.id, value: $scope.workflow.name});
                        $window.close();
                    })
                    .error(function (result) {
                        $scope.errors = result;
                    })
            } else {
                WorkflowFactory.update($scope.workflow)
                    .success(function (result) {
                        $window.opener.workflow({id: $scope.workflow.id, value: $scope.workflow.name});
                        $window.close();
                    })
                    .error(function (result) {
                        $scope.errors = result;
                    })
            }
        }

        $scope.isEmpty = function (obj) {
            for (var i in obj) if (obj.hasOwnProperty(i)) return false;
            return true;
        };

        if (id == undefined) {
            WorkflowFactory.create({name: 'New workflow'})
                .success(function (result) {
                    $scope.workflow = result;
                    $scope.loading = false;

                    angular.forEach($scope.workflow.states, function (state) {
                        for (var i = 0; i < state.available_states.length; i++) {
                            state.available_states[i] = String(state.available_states[i]);
                        }
                    });
                });
        } else {
            WorkflowFactory.get(id)
                .success(function (result) {
                    $scope.workflow = result;
                    $scope.loading = false;

                    angular.forEach($scope.workflow.states, function (state) {
                        for (var i = 0; i < state.available_states.length; i++) {
                            state.available_states[i] = String(state.available_states[i]);
                        }
                    });
                });
        }


    }])
    .factory('WorkflowFactory', ['$http', function($http) {

        var urlBase = '/workflow/api/';
        var dataFactory = {};

        dataFactory.get = function (projectId) {
            return $http.get(urlBase + projectId);
        };

        dataFactory.update = function (workflow) {
            return $http.put(urlBase + workflow.id, workflow);
        };

        dataFactory.updateStatus = function (status) {
            return $http.put(urlBase + 'status/' + status.id, status);
        };

        dataFactory.createStatus = function (status) {
            return $http.post(urlBase + 'status/', status);
        };

        dataFactory.remove = function (workflow) {
            return $http.delete(urlBase + workflow.id, workflow);
        };

        dataFactory.create = function (workflow) {
            return $http.post(urlBase + 'create/', workflow);
        };

        dataFactory.bind = function (workflow, projectId) {
            return $http.put(urlBase + workflow.id + '/' + projectId, workflow);
        };

        return dataFactory;
    }]);