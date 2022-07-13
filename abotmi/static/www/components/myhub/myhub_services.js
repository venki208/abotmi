angular.module('myhub_services',[])

.service('MyHubShareData',function(){
    var share = this;
    var applycrisil = {};
    var paycrisil = {};
    var loopedadvisorslist = {};
    var viewenquiries = {};
    var dashboarddetails = {};
    var transactiondetails = {};
    var memberlist = {};
    var invitedmemberlist = {};
    var viewraterankdetails = {};
    var ratepeerlist = {};
    var ratepeer = {};

    share.setApplyCrisil = function(data){
        applycrisil = data;
    };

    share.getApplyCrisil = function(){
        return applycrisil;
    };

    share.setPayCrisil = function(data){
        paycrisil = data;
    };

    share.getPayCrisil = function(){
        return paycrisil;
    };

    share.setLoopedAdvisors = function(data){
        loopedadvisorslist = data;
    };

    share.getLoopedAdvisors = function(){
        return loopedadvisorslist;
    };

    share.setViewEnquiries = function(data){
        viewenquiries = data;
    };

    share.getViewEnquiries = function(){
        return viewenquiries;
    };

    share.setDashboardDetails = function(data){
        dashboarddetails = data;
    };

    share.getDashboardDetails = function(){
        return dashboarddetails;
    };

    share.setViewTransactions = function(data){
        transactiondetails = data;
    };

    share.getViewTransactions = function(){
        return transactiondetails;
    };

    share.setViewMembers = function(data){
        memberlist = data;
    };

    share.getViewMembers = function(){
        return memberlist;
    };

    share.setViewInvitedMembers = function(data){
        invitedmemberlist = data;
    };

    share.getViewInvitedMembers = function(){
        return invitedmemberlist;
    };

    share.setViewRateRankDetails = function(data,type){
        viewraterankdetails = data;
        if(type == "advisor"){
            viewraterankdetails.type = "View Peers";
        }else{
            viewraterankdetails.type = "View Clients"
        }
    };

    share.getViewRateRankDetails = function(){
        return viewraterankdetails;
    };

    share.setRatePeerList = function(data){
        ratepeerlist = data;
    };

    share.getRatePeerList = function(){
        return ratepeerlist;
    };

    share.setRatePeer = function(data){
        ratepeer = data;
    };

    share.getRatePeer = function(){
        return ratepeer;
    };
})
