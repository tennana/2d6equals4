<tableSelectButton>
	<div class="btn-group btn-block" hide={ decision || opts.GMData.gmTableId == opts.dataTableid}>
		<button class="btn btn-primary selectBtn" data-target="oneTableID" onclick={selectClick}>
			<i class="glyphicon glyphicon-ok-sign" if={this.oneTableID == opts.dataTableid}></i>
			第一希望
		</button>
		<button class="btn selectBtn" data-target="twoTableID" onclick={selectClick}>
			<i class="glyphicon glyphicon-ok-sign" if={this.twoTableID == opts.dataTableid}></i>
			第二希望
		</button>
	</div>
	<script>
		this.oneTableID = opts.oneTableID || '';
		this.twoTableID = opts.twoTableID || '';
		this.decision = opts.decision;
		window.on("update",function(opts){
			this.oneTableID = opts.oneTableID;
			this.twoTableID = opts.twoTableID;
			this.decision = opts.decision || this.decision;
			this.update();
		}.bind(this));

		selectClick(e){
			var updateStatus = {"oneTableID":this.oneTableID,"twoTableID":this.twoTableID};
			var target = e.target.getAttribute("data-target");
			if(updateStatus[target] == opts.dataTableid) return;
			if(!confirm(this.getTableName(opts.dataTableid)+"を希望しますか?")) return;
			if(this.oneTableID == opts.dataTableid){
				this.oneTableID = (updateStatus["oneTableID"] = null);
			}
			if(this.twoTableID == opts.dataTableid){
				this.twoTableID = (updateStatus["twoTableID"] = null);
			}
			updateStatus[target] = opts.dataTableid;
			$.ajax({
				type: 'POST',
				url: "./wish",
				data: jQuery.param(updateStatus)
			});
			window.trigger("update",updateStatus);
		}

		getTableName(tableID){
			if(tableID === undefined) return "未選択";
			for( var i in opts.info){
				if(opts.info[i].tableID == tableID){
					return opts.info[i].tableName;
				}
			}
			return "未選択";
		}
	</script>
</tableSelectButton>
