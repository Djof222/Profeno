/** @odoo-module **/
import { registry } from "@web/core/registry"
import { loadBundle } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onMounted,onWillStart } from  "@odoo/owl";

// const { Component } = owl
export class Dashboard extends Component {
	setup(){
		console.log("odoo wol owl services ");
		this.rpc = useService("rpc");
		this.actionService = useService("action");
		
		
		onWillStart( () => {
			 loadBundle({
					jsLibs: [
						'/web/static/lib/Chart/Chart.js',
						]
					});
			var self=this
			return $.when(
				loadBundle(this),
				).then(function () {
				return self.render_connection_cards()
			})
			});

		onMounted(() => {
			this.render_recent_lead_chart();
			this.render_total_lead_chart();
		  });
	}

	on_attach_callback(){
					this.render_recent_lead_chart();
					this.render_total_lead_chart();
				}

	render_connection_cards(){
					var self = this
					return this.rpc('/multichannel_crm/fetch_connection_data'
					).then(function (result) {
						self.connections = result
					})
				}	

	render_recent_lead_chart(){
					this.rpc('/multichannel_crm/fetch_recent_lead_data',{
						period: $('#recent_lead_period option:selected').val()}
					).then(function (result) {
						$('#recent_lead_chart').replaceWith($('<canvas/>',{id: 'recent_lead_chart'}))
						new Chart('recent_lead_chart', {
							type: 'bar',
							data: {
								labels: result.map(i=>i.label),
								datasets: [{
									data: result.map(i=>i.count),
									backgroundColor:'#3e95cd',
									barPercentage: 0.2,
								}]
							},
							options: {
								maintainAspectRatio: false,
								responsive: true,
								legend: {
									display: false,
								},
								scales: {
									x: {
										display:true
									},
									y: {
										display: false,
										ticks: {
											precision: 0,
											beginAtZero: true,
										},
									},
								}
							}
						})
					})
				}

	render_total_lead_chart(){
					this.rpc('/multichannel_crm/fetch_total_lead_data'
					).then(function (result) {
						$('#total_lead_chart').replaceWith($('<canvas/>',{id: 'total_lead_chart'}))
						new Chart('total_lead_chart',{
							type: 'pie',
							data: {
								labels: result.map(i=>i.name.en_US),
								datasets: [{
									data: result.map(i=>i.count),
									backgroundColor: result.map(i=>i.color),
								}],
							},
							options: {
								maintainAspectRatio: false,
								responsive: true,
								cutoutPercentage: 75,
								legend: {
									position: 'top',
									labels: {
										usePointStyle: true,
									},
								},
							},
						})
					})
				}

}
Dashboard.template =  "template_dashboard"
registry.category("actions").add("tag_dashboard",Dashboard)


export class ConnectionDashboard extends Component {
	setup(){
		this.rpc = useService("rpc");
		onWillStart( () => {
			loadBundle({
				   jsLibs: [
					   '/web/static/lib/Chart/Chart.js',
					   ]
				   });
		   var self=this
		   return $.when(
			   loadBundle(this),
			   ).then(function () {
			   return self.render_connection_card()
		   })
		   });
	   onMounted(() => {
			this.render_recent_lead_chart();
					this.render_total_lead_chart();
					this.render_top_user_chart();
		  });
	}
	render_connection_card(){
					var self = this
					return this.rpc(`/multichannel_crm/fetch_connection_data/${this.id}`,
					).then(function (result) {
						self.connection = result
					})
				}

	on_attach_callback(){
					this.render_recent_lead_chart()
					this.render_total_lead_chart()
					this.render_top_user_chart()
				}

	

	render_recent_lead_chart(){
					this.rpc(`/multichannel_crm/fetch_recent_lead_data/${this.id}`,
						{period: $('#recent_lead_period option:selected').val()}
	).then(function (result) {
						$('#connection_recent_lead_chart').replaceWith($('<canvas/>',{id: 'connection_recent_lead_chart'}))
						new Chart(document.getElementById('connection_recent_lead_chart'), {
							type: 'bar',
							data: {
								labels: result.data.map(i=>i.label),
								datasets: [{
									data: result.data.map(i=>i.count),
									backgroundColor:result.color,
								}]
							},
							options: {
								maintainAspectRatio: false,
								responsive: true,
								legend: {
									display: false,
								},
								scales: {
									x: {
										display: false,
										barPercentage: 0.2,
									},
									y: {
										display: false,
										ticks: {
											precision: 0,
											beginAtZero: true,
										},
									},
								}
							}
						})
					})
				}


	render_total_lead_chart(){
							this.rpc(`/multichannel_crm/fetch_total_lead_data/${this.id}`,
							).then(function (result) {
								$('#connection_total_lead_chart').replaceWith($('<canvas/>',{id: 'connection_total_lead_chart'}))
								new Chart('connection_total_lead_chart',{
									type: 'pie',
									data: {
										labels: result.map(i=>i.name.en_US),
										datasets: [{
											data: result.map(i=>i.count),
											backgroundColor: result.map(i=>i.color),
										}],
									},
									options: {
										maintainAspectRatio: false,
										responsive: true,
										cutoutPercentage: 75,
										legend: {
											labels: {
												usePointStyle: true,
											},
										},
									},
								})
							})
						}

	render_top_user_chart(){

					this.rpc(`/multichannel_crm/fetch_top_user_data/${this.id}`,
					).then(function (result) {
						$('#top_user_chart').replaceWith($('<canvas/>',{id: 'top_user_chart'}))
						var users = result.users
						var names = users.map(i => i['name'])
						var datasets = Object.entries(result.data).map(
							i => ({
								label: i[0],
								data: users.map(j => i[1][j['id']]),
								backgroundColor: result.colors[i[0]],
							})
						)
						document.getElementById('top_user_chart').height = names.length * 30+60;
						new Chart('top_user_chart',{
							type: 'horizontalBar',
							data: {
								labels: names,
								datasets: datasets,
							},
							options: {
								maintainAspectRatio: false,
								responsive: true,
								scales: {
									xAxes: [{
										stacked: true,
										gridLines: {
											display: false,
										},
										ticks: {
											beginAtZero: true,
											display: false,
										},
									}],
									yAxes: [{
										stacked: true,
										gridLines: {
											display: false,
										},
									}]
								}
							},
						})
					})
				}

	on_action(e){
					e.preventDefault()
					var target = $(e.currentTarget)
					var connection_id = target.data('connection')
					var action = target.data('action')
		
					switch (action) {
						case 'import':
							return this.actionService.doAction('odoo_multi_channel_crm.action_channel_import_wizard', {
								additional_context: {
									default_connection_id: connection_id,
								},
							})
						case 'open':
							return this.actionService.doAction({
								name: 'Connection',
								type: 'ir.actions.act_window',
								res_model: 'channel.connection',
								res_id: connection_id,
								views: [[false,'form']],
								target: 'main'
							})
					}
				}
						
}
ConnectionDashboard.template =  "template_connection_dashboard"
registry.category("actions").add("connection_dashboard",ConnectionDashboard)

	
