angular.module('workflow', ['workflow.urls'])
    .config(['$httpProvider', function($httpProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ])
    .controller('WorkflowController', ['$scope', '$window', 'workflowId', 'WorkflowFactory', function($scope, $window, workflowId, WorkflowFactory) {

        $scope.workflow = undefined;
        $scope.loading = true;

        $scope.addStatus = function() {
            var found = false;
            angular.forEach($scope.workflow.states, function(obj){
                if (obj.name === undefined)
                    found = true;
            });
            if (!found)
                $scope.workflow.states.push({
                    name: '',
                    type: 2
                })
        }

        $scope.send = function() {
            angular.forEach($scope.workflow.states, function(state) {
                var _state = angular.copy(state);
                for (var i = 0; i < state.available_states.length; i++) {
                    state.available_states[i] = Number(state.available_states[i]);
                }
                /*WorkflowFactory.updateStatus(_state)
                    .success(function() {

                    })*/
            })
            WorkflowFactory.update($scope.workflow)
                .success(function(result) {
                    $window.opener.workflow({id: workflowId, value: $scope.workflow.name});
                    $window.close();
                })
                .error(function(result) {
                    alert('Error');
                })
        }

        WorkflowFactory.get(workflowId)
            .success(function(result) {
                $scope.workflow = result;
                $scope.loading = false;

                angular.forEach($scope.workflow.states, function(state) {
                    for (var i = 0; i < state.available_states.length; i++) {
                        state.available_states[i] = String(state.available_states[i]);
                    }
                });
            });
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

        dataFactory.remove = function (workflow) {
            return $http.delete(urlBase + workflow.id, workflow);
        };

        dataFactory.create = function (workflow) {
            return $http.post(urlBase, event);
        };

        return dataFactory;
    }]);