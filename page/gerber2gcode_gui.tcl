#############################################################################
# Generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#  Dec 04, 2019 05:49:43 PM CET  platform: Windows NT
set vTcl(timestamp) ""


if {!$vTcl(borrow) && !$vTcl(template)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #ececec
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(active_menu_fg) #000000
}




proc vTclWindow.top42 {base} {
    global vTcl
    if {$base == ""} {
        set base .top42
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -menu "$top.m43" -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 800x580+606+313
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 800 600
    wm minsize $top 800 600
    wm overrideredirect $top 0
    wm resizable $top 0 0
    wm deiconify $top
    wm title $top "GERBER2GCODE - Solder paste dispenser for 3D printer"
    vTcl:DefineAlias "$top" "main_window" vTcl:Toplevel:WidgetProc "" 1
    set site_3_0 $top.m43
    menu $site_3_0 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(pr,menubgcolor) -font TkMenuFont \
        -foreground $vTcl(pr,menufgcolor) -tearoff 0 
    vTcl:DefineAlias "$site_3_0" "gui_menubar" vTcl:WidgetProc "" 1
    $site_3_0 add cascade \
        -menu "$site_3_0.men51" -activebackground $vTcl(analog_color_m) \
        -activeforeground #000000 -background $vTcl(pr,menubgcolor) \
        -command {{}} -compound none -font TkMenuFont \
        -foreground $vTcl(pr,menufgcolor) -label File 
    menu $site_3_0.men51 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(pr,menubgcolor) -font {-family {Segoe UI} -size 9} \
        -foreground black -tearoff 0 
    $site_3_0.men51 add command \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(pr,menubgcolor) -command {#gui_button_exit} \
        -font TkMenuFont -foreground $vTcl(pr,menufgcolor) -label Exit 
    $site_3_0 add cascade \
        -menu "$site_3_0.men51" -activebackground $vTcl(analog_color_m) \
        -activeforeground #000000 -background $vTcl(pr,menubgcolor) \
        -command {{}} -compound none -font TkMenuFont \
        -foreground $vTcl(pr,menufgcolor) -label File -menu "$site_3_0.men44" \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(pr,menubgcolor) -command {{}} -compound left \
        -font {} -foreground $vTcl(pr,menufgcolor) -label Settings 
    menu $site_3_0.men44 \
        -activebackground #f9f9f9 -activeforeground black \
        -background $vTcl(pr,menubgcolor) -font {-family {Segoe UI} -size 9} \
        -foreground black -tearoff 0 
    $site_3_0.men44 add command \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(pr,menubgcolor) -command {#gui_button_loadsettings} \
        -font {} -foreground $vTcl(pr,menufgcolor) -label Load 
    $site_3_0.men44 add command \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(pr,menubgcolor) -command {#gui_button_savesettings} \
        -font {} -foreground $vTcl(pr,menufgcolor) -label Save 
    $site_3_0.men44 add separator \
        -background $vTcl(pr,menubgcolor) 
    $site_3_0.men44 add command \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(pr,menubgcolor) \
        -command {#gui_button_resetsettings} -font {} \
        -foreground $vTcl(pr,menufgcolor) -label Reset 
    ttk::style configure TNotebook -background $vTcl(actual_gui_bg)
    ttk::style configure TNotebook.Tab -background $vTcl(actual_gui_bg)
    ttk::style configure TNotebook.Tab -foreground $vTcl(actual_gui_fg)
    ttk::style configure TNotebook.Tab -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::style map TNotebook.Tab -background [list disabled $vTcl(actual_gui_bg) selected $vTcl(pr,guicomplement_color)]
    ttk::notebook $top.tNo70 \
        -width 804 -height 606 -takefocus {} 
    vTcl:DefineAlias "$top.tNo70" "gui_notebook" vTcl:WidgetProc "main_window" 1
    frame $top.tNo70.t0 \
        -relief groove -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.tNo70.t0" "gui_notebook_t0" vTcl:WidgetProc "main_window" 1
    $top.tNo70 add $top.tNo70.t0 \
        -padding 0 -sticky nsew -state normal -text Main -image {} \
        -compound left -underline -1 
    set site_4_0  $top.tNo70.t0
    labelframe $site_4_0.lab75 \
        -font TkDefaultFont -foreground black -text Preview \
        -background $vTcl(actual_gui_bg) -height 540 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 520 
    vTcl:DefineAlias "$site_4_0.lab75" "gui_labelframe_preview" vTcl:WidgetProc "main_window" 1
    set site_5_0 $site_4_0.lab75
    canvas $site_5_0.can64 \
        -background #ffffff -borderwidth 2 -closeenough 1.0 -height 400 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -relief ridge -selectbackground #c4c4c4 \
        -selectforeground black -width 400 
    vTcl:DefineAlias "$site_5_0.can64" "gui_preview_canvas" vTcl:WidgetProc "main_window" 1
    radiobutton $site_5_0.rad60 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -anchor w -background $vTcl(actual_gui_bg) \
        -command gui_preview_changesides -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text {Top side} -value a 
    vTcl:DefineAlias "$site_5_0.rad60" "gui_preview_top" vTcl:WidgetProc "main_window" 1
    radiobutton $site_5_0.rad61 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -anchor w -background $vTcl(actual_gui_bg) \
        -command gui_preview_changesides -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text {Bottom side} -value b 
    vTcl:DefineAlias "$site_5_0.rad61" "gui_preview_bottom" vTcl:WidgetProc "main_window" 1
    place $site_5_0.can64 \
        -in $site_5_0 -x 10 -y 20 -width 500 -relwidth 0 -height 500 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.rad60 \
        -in $site_5_0 -x 10 -y 520 -width 98 -relwidth 0 -height 15 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.rad61 \
        -in $site_5_0 -x 110 -y 520 -width 98 -relwidth 0 -height 15 \
        -relheight 0 -anchor nw -bordermode ignore 
    labelframe $site_4_0.lab52 \
        -font TkDefaultFont -foreground black -text Import \
        -background $vTcl(actual_gui_bg) -height 165 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 250 
    vTcl:DefineAlias "$site_4_0.lab52" "gui_labelframe_import" vTcl:WidgetProc "main_window" 1
    set site_5_0 $site_4_0.lab52
    button $site_5_0.but53 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command gui_button_importGerber \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text {Import GERBER file...} 
    vTcl:DefineAlias "$site_5_0.but53" "gui_button_importGerber" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab52 \
        -anchor w -background $vTcl(actual_gui_bg) \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) -text {PCB size on X axis (mm)} 
    vTcl:DefineAlias "$site_5_0.lab52" "Label_PCBSizeX" vTcl:WidgetProc "main_window" 1
    entry $site_5_0.ent53 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -state readonly -textvariable gui_srcpcbxsize 
    vTcl:DefineAlias "$site_5_0.ent53" "gui_srcpcbxsize" vTcl:WidgetProc "main_window" 1
    entry $site_5_0.ent54 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -state readonly -textvariable gui_srcpcbysize 
    vTcl:DefineAlias "$site_5_0.ent54" "gui_srcpcbysize" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab55 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {PCB size on Y axis (mm)} 
    vTcl:DefineAlias "$site_5_0.lab55" "Label_PCBSizeY" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab56 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {Source format} 
    vTcl:DefineAlias "$site_5_0.lab56" "Label_SourceFormat" vTcl:WidgetProc "main_window" 1
    entry $site_5_0.ent57 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -state readonly -textvariable gui_srcformat 
    vTcl:DefineAlias "$site_5_0.ent57" "gui_srcformat" vTcl:WidgetProc "main_window" 1
    place $site_5_0.but53 \
        -in $site_5_0 -x 20 -y 30 -width 207 -relwidth 0 -height 34 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab52 \
        -in $site_5_0 -x 10 -y 100 -width 132 -relwidth 0 -height 41 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.ent53 \
        -in $site_5_0 -x 160 -y 110 -width 64 -relwidth 0 -height 20 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.ent54 \
        -in $site_5_0 -x 160 -y 130 -width 64 -relwidth 0 -height 20 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab55 \
        -in $site_5_0 -x 10 -y 130 -width 132 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab56 \
        -in $site_5_0 -x 10 -y 90 -width 132 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.ent57 \
        -in $site_5_0 -x 160 -y 90 -width 64 -relwidth 0 -height 20 \
        -relheight 0 -anchor nw -bordermode ignore 
    labelframe $site_4_0.lab48 \
        -font TkDefaultFont -foreground black -text {PCB origin} \
        -background $vTcl(actual_gui_bg) -height 105 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 250 
    vTcl:DefineAlias "$site_4_0.lab48" "gui_labelframe_pcborigin" vTcl:WidgetProc "main_window" 1
    set site_5_0 $site_4_0.lab48
    spinbox $site_5_0.spi60 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -command gui_3dp_updatedorigin -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground black -format %1.1f -from 0.0 \
        -highlightbackground black -highlightcolor black -increment 0.1 \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable gui_3dp_pcbxorig -to 100.0 
    vTcl:DefineAlias "$site_5_0.spi60" "gui_3dp_pcbxorig" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab61 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {On X axis (mm)} 
    vTcl:DefineAlias "$site_5_0.lab61" "Label_PCBOriginX" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab62 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {On Y axis (mm)} 
    vTcl:DefineAlias "$site_5_0.lab62" "Label_PCBOriginY" vTcl:WidgetProc "main_window" 1
    spinbox $site_5_0.spi63 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -command gui_3dp_updatedorigin -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground black -format %1.1f -from 0.0 \
        -highlightbackground black -highlightcolor black -increment 0.1 \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable gui_3dp_pcbyorig -to 100.0 
    vTcl:DefineAlias "$site_5_0.spi63" "gui_3dp_pcbyorig" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab46 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {On Z axis (mm)} 
    vTcl:DefineAlias "$site_5_0.lab46" "Label_PCBOriginZ" vTcl:WidgetProc "main_window" 1
    spinbox $site_5_0.spi47 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -command gui_3dp_updatedorigin -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground black -format %1.2f -from 0.0 \
        -highlightbackground black -highlightcolor black -increment 0.1 \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable gui_3dp_pcbzorig -to 100.0 
    vTcl:DefineAlias "$site_5_0.spi47" "gui_3dp_pcbzorig" vTcl:WidgetProc "main_window" 1
    place $site_5_0.spi60 \
        -in $site_5_0 -x 180 -y 30 -width 55 -relwidth 0 -height 19 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab61 \
        -in $site_5_0 -x 10 -y 30 -width 84 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab62 \
        -in $site_5_0 -x 10 -y 50 -width 84 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.spi63 \
        -in $site_5_0 -x 180 -y 50 -width 55 -relwidth 0 -height 19 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab46 \
        -in $site_5_0 -x 10 -y 70 -width 84 -height 21 -anchor nw \
        -bordermode ignore 
    place $site_5_0.spi47 \
        -in $site_5_0 -x 180 -y 70 -width 55 -height 19 -anchor nw \
        -bordermode ignore 
    labelframe $site_4_0.lab49 \
        -font TkDefaultFont -foreground black -text {Number of PCBs} \
        -background $vTcl(actual_gui_bg) -height 85 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 250 
    vTcl:DefineAlias "$site_4_0.lab49" "gui_labelframe_numberpcbs" vTcl:WidgetProc "main_window" 1
    set site_5_0 $site_4_0.lab49
    spinbox $site_5_0.spi60 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -command gui_3dp_updatedcount -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground black -from 1.0 \
        -highlightbackground black -highlightcolor black -increment 1.0 \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable gui_3dp_pcbxcount -to 10.0 
    vTcl:DefineAlias "$site_5_0.spi60" "gui_3dp_pcbxcount" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab61 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {On X axis} 
    vTcl:DefineAlias "$site_5_0.lab61" "Label_PCBCountX" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab62 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {On Y axis} 
    vTcl:DefineAlias "$site_5_0.lab62" "Label_PCBCountY" vTcl:WidgetProc "main_window" 1
    spinbox $site_5_0.spi63 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -command gui_3dp_updatedcount -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground black -from 1.0 \
        -highlightbackground black -highlightcolor black -increment 1.0 \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable gui_3dp_pcbycount -to 10.0 
    vTcl:DefineAlias "$site_5_0.spi63" "gui_3dp_pcbycount" vTcl:WidgetProc "main_window" 1
    place $site_5_0.spi60 \
        -in $site_5_0 -x 180 -y 30 -width 55 -relwidth 0 -height 19 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab61 \
        -in $site_5_0 -x 10 -y 30 -width 84 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab62 \
        -in $site_5_0 -x 10 -y 50 -width 84 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.spi63 \
        -in $site_5_0 -x 180 -y 50 -width 55 -relwidth 0 -height 19 \
        -relheight 0 -anchor nw -bordermode ignore 
    labelframe $site_4_0.lab64 \
        -font TkDefaultFont -foreground black \
        -text {PCB furthest coordinate (oposite of origin)} \
        -background $vTcl(actual_gui_bg) -height 85 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 250 
    vTcl:DefineAlias "$site_4_0.lab64" "gui_labelframe_furthestpcbcoordinate" vTcl:WidgetProc "main_window" 1
    set site_5_0 $site_4_0.lab64
    label $site_5_0.lab61 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {On X axis (mm)} 
    vTcl:DefineAlias "$site_5_0.lab61" "Label_PCBFurthestX" vTcl:WidgetProc "main_window" 1
    label $site_5_0.lab62 \
        -activebackground #f9f9f9 -activeforeground black -anchor w \
        -background $vTcl(actual_gui_bg) -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text {On Y axis (mm)} 
    vTcl:DefineAlias "$site_5_0.lab62" "Label_PCBFurthestY" vTcl:WidgetProc "main_window" 1
    spinbox $site_5_0.spi65 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -command gui_3dp_updatedfurthest -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground black -format %1.1f -from 0.0 \
        -highlightbackground black -highlightcolor black -increment 0.1 \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable gui_3dp_pcbxfurthest -to 100.0 
    vTcl:DefineAlias "$site_5_0.spi65" "gui_3dp_pcbxfurthest" vTcl:WidgetProc "main_window" 1
    spinbox $site_5_0.spi66 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -command gui_3dp_updatedfurthest -disabledforeground #a3a3a3 \
        -font TkDefaultFont -foreground black -format %1.1f -from 0.0 \
        -highlightbackground black -highlightcolor black -increment 0.1 \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable gui_3dp_pcbyfurthest -to 100.0 
    vTcl:DefineAlias "$site_5_0.spi66" "gui_3dp_pcbyfurthest" vTcl:WidgetProc "main_window" 1
    place $site_5_0.lab61 \
        -in $site_5_0 -x 10 -y 30 -width 84 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.lab62 \
        -in $site_5_0 -x 10 -y 50 -width 84 -relwidth 0 -height 21 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.spi65 \
        -in $site_5_0 -x 180 -y 30 -width 55 -height 19 -anchor nw \
        -bordermode ignore 
    place $site_5_0.spi66 \
        -in $site_5_0 -x 180 -y 50 -width 55 -height 19 -anchor nw \
        -bordermode ignore 
    place $site_4_0.lab75 \
        -in $site_4_0 -x 270 -y 10 -width 520 -relwidth 0 -height 540 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.lab52 \
        -in $site_4_0 -x 10 -y 10 -width 250 -relwidth 0 -height 165 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.lab48 \
        -in $site_4_0 -x 10 -y 180 -width 250 -relwidth 0 -height 105 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.lab49 \
        -in $site_4_0 -x 10 -y 290 -width 250 -relwidth 0 -height 85 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_0.lab64 \
        -in $site_4_0 -x 10 -y 380 -width 250 -height 85 -anchor nw \
        -bordermode ignore 
    frame $top.tNo70.t3 \
        -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.tNo70.t3" "gui_notebook_t1" vTcl:WidgetProc "main_window" 1
    $top.tNo70 add $top.tNo70.t3 \
        -padding 0 -sticky nsew -state normal -text {G-code settings} \
        -image {} -compound none -underline -1 
    set site_4_1  $top.tNo70.t3
    labelframe $site_4_1.lab56 \
        -font TkDefaultFont -foreground black -text {Initial settings} \
        -background $vTcl(actual_gui_bg) -height 265 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 380 
    vTcl:DefineAlias "$site_4_1.lab56" "gui_gcode_labelframe_initial" vTcl:WidgetProc "main_window" 1
    set site_5_0 $site_4_1.lab56
    checkbutton $site_5_0.che58 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -anchor w -background $vTcl(actual_gui_bg) \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -justify left -text {Auto-home (G28)} -variable che58 
    vTcl:DefineAlias "$site_5_0.che58" "gui_checkbutton_gcode_autohome" vTcl:WidgetProc "main_window" 1
    entry $site_5_0.ent63 \
        -background white -disabledforeground #a3a3a3 -font TkFixedFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black 
    vTcl:DefineAlias "$site_5_0.ent63" "Entry1" vTcl:WidgetProc "main_window" 1
    spinbox $site_5_0.spi64 \
        -activebackground #f9f9f9 -background white -buttonbackground #d9d9d9 \
        -disabledforeground #a3a3a3 -font TkDefaultFont -foreground black \
        -from 1.0 -highlightbackground black -highlightcolor black \
        -increment 1.0 -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable spinbox -to 20.0 
    vTcl:DefineAlias "$site_5_0.spi64" "Spinbox1" vTcl:WidgetProc "main_window" 1
    place $site_5_0.che58 \
        -in $site_5_0 -x 10 -y 30 -width 211 -relwidth 0 -height 15 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_5_0.ent63 \
        -in $site_5_0 -x 80 -y 120 -anchor nw -bordermode ignore 
    place $site_5_0.spi64 \
        -in $site_5_0 -x 320 -y 30 -width 45 -relwidth 0 -height 19 \
        -relheight 0 -anchor nw -bordermode ignore 
    labelframe $site_4_1.lab57 \
        -font TkDefaultFont -foreground black -text {Final settings} \
        -background $vTcl(actual_gui_bg) -height 165 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 380 
    vTcl:DefineAlias "$site_4_1.lab57" "gui_gcode_labelframe_final" vTcl:WidgetProc "main_window" 1
    place $site_4_1.lab56 \
        -in $site_4_1 -x 10 -y 10 -width 380 -relwidth 0 -height 265 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_1.lab57 \
        -in $site_4_1 -x 410 -y 10 -width 380 -relwidth 0 -height 165 \
        -relheight 0 -anchor nw -bordermode ignore 
    frame $top.tNo70.t1 \
        -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.tNo70.t1" "gui_notebook_t2" vTcl:WidgetProc "main_window" 1
    $top.tNo70 add $top.tNo70.t1 \
        -padding 0 -sticky nsew -state normal -text {3D printer} -image {} \
        -compound left -underline -1 
    set site_4_2  $top.tNo70.t1
    frame $top.tNo70.t2 \
        -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    vTcl:DefineAlias "$top.tNo70.t2" "gui_notebook_t3" vTcl:WidgetProc "main_window" 1
    $top.tNo70 add $top.tNo70.t2 \
        -padding 0 -sticky nsew -state normal -text Log -image {} \
        -compound none -underline -1 
    set site_4_3  $top.tNo70.t2
    text $site_4_3.tex74 \
        -background white -exportselection 0 -font TkTextFont \
        -foreground black -height 504 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -width 774 -wrap word 
    .top42.tNo70.t2.tex74 configure -font "TkTextFont"
    .top42.tNo70.t2.tex74 insert end text
    vTcl:DefineAlias "$site_4_3.tex74" "gui_log_window" vTcl:WidgetProc "main_window" 1
    button $site_4_3.but76 \
        -activebackground $vTcl(analog_color_m) -activeforeground #000000 \
        -background $vTcl(actual_gui_bg) -command gui_button_clearlog \
        -disabledforeground #a3a3a3 -font TkDefaultFont \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -pady 0 -text {Clear log} 
    vTcl:DefineAlias "$site_4_3.but76" "gui_button_clearlog" vTcl:WidgetProc "main_window" 1
    place $site_4_3.tex74 \
        -in $site_4_3 -x 10 -y 40 -width 774 -relwidth 0 -height 504 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_4_3.but76 \
        -in $site_4_3 -x 10 -y 10 -width 77 -relwidth 0 -height 24 \
        -relheight 0 -anchor nw -bordermode ignore 
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.tNo70 \
        -in $top -x 0 -y 0 -width 804 -relwidth 0 -height 606 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top42 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}

