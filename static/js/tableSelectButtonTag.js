riot.tag2('tableselectbutton', '<div class="btn-group btn-block" hide="{decision || opts.GMData.gmTableId == opts.dataTableid}"> <button class="btn btn-primary selectBtn" data-target="oneTableID" onclick="{selectClick}"> <i class="glyphicon glyphicon-ok-sign" if="{this.oneTableID == opts.dataTableid}"></i> 第一希望 </button> <button class="btn selectBtn" data-target="twoTableID" onclick="{selectClick}"> <i class="glyphicon glyphicon-ok-sign" if="{this.twoTableID == opts.dataTableid}"></i> 第二希望 </button> </div>', '', '', function(opts) {
		this.oneTableID = opts.oneTableID || '';
		this.twoTableID = opts.twoTableID || '';
		this.decision = opts.decision;
		window.on("update",function(opts){
			this.oneTableID = opts.oneTableID || this.oneTableID;
			this.twoTableID = opts.twoTableID || this.twoTableID;
			this.decision = opts.decision || this.decision;
			this.update();
		}.bind(this));

		this.selectClick = function(e){
			var updateStatus = $({},opts,true);
			var target = e.target.getAttribute("data-target");
			updateStatus[target] = opts.dataTableid;
			window.trigger("update",updateStatus);
		}.bind(this)
});
