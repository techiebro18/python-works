// @hash v3-390CEEE86888AC98F641FE9D7B3C9C2C39BD2612
// Automatically generated by ReactJS.NET. Do not edit, your changes will be overridden.
// Version: 3.0.1 (build 0) with Babel 6.7.7
// Generated at: 11/22/2020 2:31:26 AM
///////////////////////////////////////////////////////////////////////////////
function healthmug(state, action) {
	if (typeof state === "undefined") var newdata = {};else var newdata = JSON.parse(JSON.stringify(state));
	if (typeof state === "undefined") {
		newdata.datalist = window.__INITIAL_STATE__;
		newdata.localdata = { selectedcombo: [], selecteddisease: null, pageno: 1, pagesize: 5 };
		newdata.localdata.selectedcombo = newdata.datalist.comboproducts.map(function (item) {
			return item.id;
		});
		newdata.localdata.devicetype = window.__DEVICE_TYPE__;
		return newdata;
	}
	if (action.type === "variantchange") {
		newdata.datalist = action.data;
		return newdata;
	}
	if (action.type === "comboupdate") {
		if (newdata.localdata.selectedcombo.indexOf(action.data) == -1) newdata.localdata.selectedcombo.push(action.data);else newdata.localdata.selectedcombo.splice(newdata.localdata.selectedcombo.indexOf(action.data), 1);
		return newdata;
	}
	if (action.type === "updatepincode") {
		localStorage.pincode = action.pincode;
		return newdata;
	}
	if (action.type === "answerquestion") {
		newdata.localdata.questionid = action.data;
		return newdata;
	}
	if (action.type === "reviewreload") {
		if (action.mode == "append") newdata.datalist.reviews.review = newdata.datalist.reviews.review.concat(action.data.review);else {
			newdata.datalist.reviews.review = action.data.review;
			newdata.datalist.reviews.reviewcount = action.data.reviewcount;
		}
		return newdata;
	}
	if (action.type === "selectdisease") {
		newdata.localdata.selecteddisease = action.data;
		return newdata;
	}
	if (action.type === "loadquestions") {
		newdata.datalist.qa.questions = newdata.datalist.qa.questions.concat(action.data.questions);
		newdata.localdata.pageno += 1;
		return newdata;
	}
	if (action.type === "append_alternatebrands") {
		newdata.datalist.alternatebrands = newdata.datalist.alternatebrands.concat(JSON.parse(action.data));
		return newdata;
	} else return state;
}
var store = Redux.createStore(healthmug);

var render = function render() {
	ReactDOM.render(React.createElement(ProductPageBlock, { datalist: store.getState().datalist, localdata: store.getState().localdata }), document.getElementById("ProductPageBlock"));
};
render();
store.subscribe(render);