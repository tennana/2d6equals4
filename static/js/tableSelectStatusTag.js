riot.tag2('tableselectstatus', '<div if="{opts.GMData.gmTableId}"> <h2>GM情報</h2> <p><a href="#tableInfo_{opts.GMData.gmTableId}">{getTableName(opts.GMData.gmTableId)}</a></p> <p>第一希望:{opts.GMData.one}人</p> <p>第二希望:{opts.GMData.two}人</p> <h3>参加者</h3> <ul><li each="{opts.GMData.player}">{name}</li></ul> </div> <div if="{!opts.decision}"> <h2>選択中の卓</h2> <p>第一希望：<br><a href="#tableInfo_{oneTableID}">{getTableName(oneTableID)}</a></p> <p>第二希望：<br><a href="#tableInfo_{twoTableID}">{getTableName(twoTableID)}</a></p> </div> <div if="{opts.decision}"> <h2>決定卓</h2> <p><a href="#tableInfo_{opts.decision}"><strong>{getTableName(opts.decision)}</strong></a></p> <h3>参加者</h3> <ul><li each="{opts.decisionPlayer}">{name}</li></ul> </div>', '', '', function(opts) {
		this.oneTableID = opts.oneTableID || '';
		this.twoTableID = opts.twoTableID || '';
		this.getTableName = function(tableID){
			if(tableID === undefined) return "未選択";
			for( var i in opts.info){
				if(opts.info[i].tableID == tableID){
					return opts.info[i].tableName;
				}
			}
			return "未選択";
		}.bind(this)
		window.on("update",function(opts){
			this.oneTableID = opts.oneTableID;
			this.twoTableID = opts.twoTableID;
			this.update();
		}.bind(this));
});
