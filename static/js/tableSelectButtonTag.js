riot.tag2('tableselectbutton', '<div class="btn-group btn-block"> <button class="btn btn-primary selectBtn" data-target="oneTableID" onclick="{selectClick}">第一希望</button> <button class="btn selectBtn" data-target="twoTableID" onclick="{selectClick}">第二希望</button> </div>', '', '', function(opts) {
		this.oneTableID = opts.oneTableID || '';
		this.twoTableID = opts.twoTableID || '';
		window.on("update",function(opts){
			this.oneTableID = opts.oneTableID || this.oneTableID;
			this.twoTableID = opts.twoTableID || this.twoTableID;
			this.update();
		}.bind(this));

		this.selectClick = function(e){
			var updateStatus = {};
			var target = e.target.getAttribute("data-target");
			updateStatus[target] = opts.dataTableid;
			window.trigger("update",updateStatus);
		}.bind(this)
});
