/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for two toolbar rows.
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for a single toolbar row.
	config.toolbarGroups = [
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'forms' },
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list' ] },
		{ name: 'links' },
        { name: 'insert'},
        { name: 'styles' },
        { name: 'colors' },
        { name: 'tools' },
        { name: 'others' }
	];

	// The default plugins included in the basic setup define some buttons that
	// are not needed in a basic editor. They are removed here.
	config.removeButtons = 'PasteText,PasteFromWord,HorizontalRule,SpecialChar,Styles,Format,Source,Cut,Copy,Paste,Undo,Redo,Anchor,Underline,Strike,Subscript,Superscript,Image';
    //config.removePlugins = 'PasteFromWord';
    //config.removeDialogTabs = 'link:advanced';
    
    // Add extra plugins
    config.extraPlugins = 'pastetext,uploader,videoembed,confighelper';
    

    config.uploadFolder = APP_URL+'/public/uploads/images/';
    config.height       = 120;
    //config.forcePasteAsPlainText = true;
    config.disableNativeSpellChecker = false;

    CKEDITOR.config.forcePasteAsPlainText = true;

    config.scayt_autoStartup = true; 
    //CKEDITOR.config.pasteFromWordCleanupFile = 'custom';
    config.pasteFromWordNumberedHeadingToList = true;
    //config.pasteFromWordPromptCleanup = true;
    config.pasteFromWordRemoveFontStyles = true;
    config.pasteFromWordRemoveStyles = true;

};



CKEDITOR.on('dialogDefinition', function(ev) {
    // Take the dialog name and its definition from the event data.
    var dialogName = ev.data.name;
    var dialogDefinition = ev.data.definition;

    // Check if the definition is from the dialog we're
    // interested in (the 'link' dialog).
    if (dialogName == 'link') {
//        Remove the 'Upload' and 'Advanced' tabs from the 'Link' dialog.
//        dialogDefinition.removeContents('upload');
//        dialogDefinition.removeContents('advanced');

        // Get a reference to the 'Link Info' tab.
        var infoTab = dialogDefinition.getContents('info');
        // Remove unnecessary widgets from the 'Link Info' tab.
        // infoTab.remove('linkType');
        infoTab.remove('protocol');
        infoTab.remove('browse');
        infoTab.get( 'linkType' ).style = 'display: none';
        // Get a reference to the "Target" tab and set default to '_blank'

        // var targetTab = dialogDefinition.getContents('target');
        // var targetField = targetTab.get('linkTargetType');
        // var targetField['default'] = '_blank';
        dialogDefinition.removeContents('target');

    }
      else if (dialogName == 'image') {
//        Remove the 'Link' and 'Advanced' tabs from the 'Image' dialog.
       dialogDefinition.removeContents('Link');
       dialogDefinition.removeContents('advanced');

        // Get a reference to the 'Image Info' tab.
        var infoTab = dialogDefinition.getContents('info');
        // Remove unnecessary widgets/elements from the 'Image Info' tab.
        //infoTab.remove('txtWidth');
        //infoTab.remove('txtHeight');
        infoTab.remove('browse');
        infoTab.remove('txtHSpace');
        infoTab.remove('txtVSpace');
        infoTab.remove('txtBorder');
        infoTab.remove('cmbAlign');
        infoTab.remove('ratioLock');

   }



    dialogDefinition = ev.data.definition;

    if (dialogName == 'image') {
        var onOk = dialogDefinition.onOk;

        dialogDefinition.onOk = function (e) {

            var maxWidth = 900;
            var maxHeight = 800;
            var ratio = 0; 

            var widthObj = this.getContentElement('info', 'txtWidth');
            width = widthObj.getValue();
            //width2 = width;
            console.log(width);

            var heightObj = this.getContentElement('info', 'txtHeight');
            height = heightObj.getValue();
            //height2 = height;
            console.log(height);

            // Check if the current width is larger than the max
            if(width > maxWidth){
                ratio   = maxWidth / width;   // get ratio for scaling image
                height  = height * ratio;    // Reset height to match scaled image
                width   = width * ratio;    // Reset width to match scaled image

                widthObj.setValue(width);
                heightObj.setValue(height);
            }

            //For height
            //console.log(width2);
            //console.log(height2);

            // Check if current height is larger than max
            /*if(height2 > maxHeight){
                ratio   = maxHeight / height2; 
                width2   = width2 * ratio;    
                height2  = height2 * ratio;   

                widthObj.setValue(width2);
                heightObj.setValue(height2);
            }*/



            onOk && onOk.apply(this, e);
        };
    }



});

