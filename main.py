from modules import *


class Inventory:
    def __init__(self, master):
        self.master = master
        self.master.title("Albany Distilling Company Inventory")
        self.master.iconbitmap('favicon.ico')
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.width = int(self.screen_width/1.2)
        self.height = int(self.screen_height/1.2)
        self.command_width = int(.33*self.width) # Command frame width
        self.table_width = int(.66*self.width) # Table frame width
        self.center_window()
        self.master.resizable(1,1)
        self.master.focus()

        # Set styles for gui and certain widgets
        self.s = ttk.Style(self.master)
        self.s.theme_use('xpnative')
        self.s.configure("Treeview", highlightthickness=0, bd=0,
                         font=('Calibri', 11)
        )
        self.s.element_create("Custom.Treeheading.border", "from", "default")
        self.s.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side':'right', 'sticky':''}),
                    ("Custom.Treeheading.text", {'sticky':'we'})
                ]})
            ]}),
        ])
        self.s.configure("Custom.Treeview.Heading",
                         background="dark slate grey", foreground="white",
                         relief="flat"
        )
        self.s.configure("Treeview.Heading", font=('Calibri', 12,'bold'))
        self.s.configure("TButton", font=('Calibri', 12,'bold'))

        # Create bottle inventory notebook, populate with tabbed frames.
        self.bottinv_nb = ttk.Notebook(self.master, height=self.height,
                                       width=self.width
        )
        self.raw_fr = ttk.Frame(self.bottinv_nb)
        self.prod_fr = ttk.Frame(self.bottinv_nb)
        self.inprog_fr = ttk.Frame(self.bottinv_nb)
        self.bott_fr = ttk.Frame(self.bottinv_nb)
        self.samp_fr = ttk.Frame(self.bottinv_nb)

        self.bottinv_nb.add(self.raw_fr, text="Raw Materials", padding=10)
        self.raw_fr.bind(
            '<Visibility>',
            lambda event:
            self.raw_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.bottinv_nb.add(self.prod_fr, text="Production Log", padding=10)
        self.prod_fr.bind(
            '<Visibility>',
            lambda event:
            view_products('production', 'All', 'All', self.prod_tbl)
        )
        self.bottinv_nb.add(self.inprog_fr, text="In Progress", padding=10)
        self.inprog_fr.bind(
            '<Visibility>',
            lambda event:
            view_products('in_progress', 'All', 'All', self.inprog_tbl)
        )
        self.bottinv_nb.add(self.bott_fr, text="Bottle Inventory", padding=10)
        self.bott_fr.bind(
            '<Visibility>',
            lambda event:
            self.bott_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.bottinv_nb.add(self.samp_fr, text="Samples", padding=10)
        self.samp_fr.bind(
            '<Visibility>',
            lambda event:
            self.samp_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.bottinv_nb.pack(side='bottom', fill='both', expand=1)

        self.raw_tbl = TreeviewTable(
            self.raw_fr, ("Type", "Product", "Amount", "Price", "Total"),
        )
        self.raw_cfr = CommandFrame(self.raw_fr)
        self.raw_vfr = ViewFrame(self.raw_cfr, 'raw_materials', self.raw_tbl)
        self.raw_optfr = OptionFrame(self.raw_cfr)
        LogisticsButton(self.raw_optfr, "Add Item", 'raw_materials',
                         self.raw_tbl,
                         lambda:
                         AddView(self.master, 'raw_materials', self.raw_tbl, 1,
                                 self.raw_vfr, self.barr_count_fr)
        )
        LogisticsButton(self.raw_optfr, "Production", 'raw_materials',
                         self.raw_tbl,
                         lambda:
                         ProductionView(self.master, 'bottles', self.raw_tbl)
        )
        LogisticsButton(self.raw_optfr, "Edit Selection", 'raw_materials',
                         self.raw_tbl,
                         lambda:
                         selection_check('raw_materials', self.raw_tbl,
                                         self.raw_vfr, self.master,
                                         self.barr_count_fr)
        )
        LogisticsButton(self.raw_optfr, "Delete Selection", 'raw_materials',
                         self.raw_tbl,
                         lambda:
                         selection_check('raw_materials', self.raw_tbl,
                                         self.raw_vfr, self.master,
                                         self.barr_count_fr, delete=True)
        )
        self.raw_optfr.pack()
        self.raw_cfr.pack(padx=10)

        self.prod_tbl = TreeviewTable(
            self.prod_fr, ("Date", "Product", "Amount"),
        )
        self.prod_cfr = CommandFrame(self.prod_fr)
        self.prod_optfr = OptionFrame(self.prod_cfr)
        LogisticsButton(self.prod_optfr, "Edit Selection", 'production',
                         self.prod_tbl,
                         lambda:
                         selection_check('production', self.prod_tbl, None,
                                         self.master, self.barr_count_fr)
        )
        LogisticsButton(self.prod_optfr, "Delete Selection", 'production',
                         self.prod_tbl,
                         lambda:
                         selection_check('production', self.prod_tbl, None,
                                         self.master, self.barr_count_fr,
                                         delete=True)
        )
        self.prod_optfr.pack()
        self.prod_cfr.pack(padx=10)

        self.inprog_tbl = TreeviewTable(
            self.inprog_fr, ("Date", "Product", "Amount", "Description"),
        )
        self.inprog_cfr = CommandFrame(self.inprog_fr)
        self.inprog_optfr = OptionFrame(self.inprog_cfr)
        LogisticsButton(self.inprog_optfr, "Finish Selection", 'in_progress',
                         self.inprog_tbl,
                         lambda:
                         selection_check(None, self.inprog_tbl, None,
                                         self.master, self.barr_count_fr)
        )
        LogisticsButton(self.inprog_optfr, "Edit Selection", 'in_progress',
                         self.inprog_tbl,
                         lambda:
                         selection_check('in_progress', self.inprog_tbl, None,
                                         self.master, self.barr_count_fr)
        )
        LogisticsButton(self.inprog_optfr, "Delete Selection", 'in_progress',
                         self.inprog_tbl,
                         lambda:
                         selection_check('in_progress', self.inprog_tbl, None,
                                         self.master, self.barr_count_fr,
                                         delete=True)
        )
        self.inprog_optfr.pack()
        self.inprog_cfr.pack(padx=10)

        self.bott_tbl = TreeviewTable(
            self.bott_fr, ("Type", "Product", "Amount", "Case Size", "Price",
                           "Total")
        )
        self.bott_cfr = CommandFrame(self.bott_fr)
        self.bott_vfr = ViewFrame(self.bott_cfr, 'bottles', self.bott_tbl)
        self.bott_optfr = OptionFrame(self.bott_cfr)
        LogisticsButton(self.bott_optfr, "Add Item", 'bottles', self.bott_tbl,
                         lambda:
                         AddView(self.master, 'bottles', self.bott_tbl, 1,
                                 self.bott_vfr, self.barr_count_fr)
        )
        LogisticsButton(self.bott_optfr, "Edit Selection", 'bottles',
                         self.bott_tbl,
                         lambda:
                         selection_check('bottles', self.bott_tbl,
                                         self.bott_vfr, self.master,
                                         self.barr_count_fr)
        )
        LogisticsButton(self.bott_optfr, "Delete Selection", 'bottles',
                         self.bott_tbl,
                         lambda:
                         selection_check('bottles', self.bott_tbl,
                                         self.bott_vfr, self.master,
                                         self.barr_count_fr, delete=True)
        )
        self.bott_optfr.pack()
        self.bott_cfr.pack(padx=10)

        self.samp_tbl = TreeviewTable(
            self.samp_fr, ("Type", "Product", "Amount", "Price", "Total")
        )
        self.samp_cfr = CommandFrame(self.samp_fr)
        self.samp_vfr = ViewFrame(self.samp_cfr, 'samples', self.samp_tbl)
        self.samp_optfr = OptionFrame(self.samp_cfr)
        LogisticsButton(self.samp_optfr, "Add Item", 'samples', self.samp_tbl,
                         lambda:
                         AddView(self.master, 'samples', self.samp_tbl, 1,
                                 self.samp_vfr, self.barr_count_fr)
        )
        LogisticsButton(self.samp_optfr,"Edit Selection",'samples',
                         self.samp_tbl,
                         lambda:
                         selection_check('samples', self.samp_tbl,
                                         self.samp_vfr, self.master,
                                         self.barr_count_fr)
        )
        LogisticsButton(self.samp_optfr, "Delete Selection", 'samples',
                         self.samp_tbl,
                         lambda:
                         selection_check('samples', self.samp_tbl,
                                         self.samp_vfr, self.master,
                                         self.barr_count_fr, delete=True)
        )
        self.samp_optfr.pack()
        self.samp_cfr.pack(padx=10)

        self.grain_nb = ttk.Notebook(self.master, height=self.height,
                                     width=self.width)
        self.grain_fr = ttk.Frame(self.grain_nb)
        self.grain_nb.add(self.grain_fr, text="Grain Inventory", padding=10)
        self.grain_fr.bind(
            '<Visibility>',
            lambda event:
            self.grain_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.mash_fr = ttk.Frame(self.grain_nb)
        self.grain_nb.add(self.mash_fr, text="Mash Log", padding=10)
        self.mash_fr.bind(
            '<Visibility>',
            lambda event:
            self.mash_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.grain_log_fr = ttk.Frame(self.grain_nb)
        self.grain_nb.add(self.grain_log_fr, text="Grain Log", padding=10)
        self.grain_log_fr.bind(
            '<Visibility>',
            lambda event:
            view_products('grain_log', 'All', 'All', self.grain_log_tbl)
        )
        self.grain_tbl = TreeviewTable(
            self.grain_fr, ("Date", "Order No", "Type", "Amount", "Price",
                            "Total")
        )
        self.grain_cfr = CommandFrame(self.grain_fr)
        self.grain_vfr = ViewFrame(self.grain_cfr, 'grain', self.grain_tbl)
        self.grain_optfr = OptionFrame(self.grain_cfr)
        LogisticsButton(self.grain_optfr, "Produce Mash", 'grain',
                         self.grain_tbl,
                         command=lambda:
                         MashProductionView(self.master, self.mash_tbl)
        )
        LogisticsButton(self.grain_optfr, "Mash Production Sheet", 'grain',
                         self.grain_tbl, None
        )
        LogisticsButton(self.grain_optfr, "Add Grain", 'grain', self.grain_tbl,
                         lambda:
                         AddView(self.master, 'grain', self.grain_tbl, 1,
                                 self.grain_vfr, self.barr_count_fr)
        )
        LogisticsButton(self.grain_optfr, "Edit Selection", 'grain',
                         self.grain_tbl,
                         lambda:
                         selection_check('grain', self.grain_tbl,
                                         self.grain_vfr, self.master,
                                         self.barr_count_fr)
        )
        LogisticsButton(self.grain_optfr, "Delete Selection", 'grain',
                         self.grain_tbl,
                         lambda:
                         selection_check('grain', self.grain_tbl,
                                         self.grain_vfr, self.master,
                                         self.barr_count_fr, delete=True)
        )
        self.grain_optfr.pack()
        self.grain_cfr.pack(padx=10)

        self.mash_tbl = TreeviewTable(
            self.mash_fr, ("Date", "Mash No", "Type", "Grains")
        )
        self.mash_cfr = CommandFrame(self.mash_fr)
        self.mash_vfr = ViewFrame(self.mash_cfr, 'mashes', self.mash_tbl)
        self.mash_optfr = OptionFrame(self.mash_cfr)
        LogisticsButton(self.mash_optfr, "Add Mash", 'mashes', self.mash_tbl,
                         lambda:
                         AddView(self.master, "mashes", self.mash_tbl, 1,
                                 self.mash_vfr, self.barr_count_fr)
        )
        LogisticsButton(self.mash_optfr, "Edit Selection", 'mashes',
                         self.mash_tbl,
                         lambda:
                         selection_check('mashes', self.mash_tbl, self.mash_vfr,
                                         self.master, self.barr_count_fr)
        )
        LogisticsButton(self.mash_optfr, "Delete Selection", 'mashes',
                         self.mash_tbl,
                         lambda:
                         selection_check('mashes', self.mash_tbl, self.mash_vfr,
                                         self.master, self.barr_count_fr,
                                         delete=True)
        )
        self.mash_optfr.pack()
        self.mash_cfr.pack(padx=10)

        self.grain_log_tbl = TreeviewTable(
            self.grain_log_fr, ("Arrival Date", "Finish Date", "Type",
                                "Order No")
        )
        self.grain_log_cfr = CommandFrame(self.grain_log_fr)
        self.grain_log_optfr = OptionFrame(self.grain_log_cfr)
        LogisticsButton(self.grain_log_optfr, "Edit Selection", 'grain_log',
                         self.grain_log_tbl,
                         lambda:
                         selection_check('grain_log', self.grain_log_tbl, None,
                                         self.master, self.barr_count_fr)
        )
        LogisticsButton(self.grain_log_optfr, "Delete Selection", 'grain_log',
                         self.grain_log_tbl,
                         lambda:
                         selection_check('grain_log', self.grain_log_tbl, None,
                                         self.master, self.barr_count_fr,
                                         delete=True)
        )
        self.grain_log_optfr.pack()
        self.grain_log_cfr.pack(padx=10)

        self.barr_nb = ttk.Notebook(self.master, height=self.height,
                                    width=self.width)
        self.barr_fr = ttk.Frame(self.barr_nb)
        self.empt_barr_fr = ttk.Frame(self.barr_nb)

        self.barr_nb.add(self.barr_fr, text="Barrel Inventory", padding=10)
        self.barr_fr.bind(
            '<Visibility>',
            lambda event:
            self.barr_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.barr_nb.add(self.empt_barr_fr, text="Emptied Barrels", padding=10)
        self.empt_barr_fr.bind(
            '<Visibility>',
            lambda event:
            view_products('empty_barrels', 'All', 'All', self.empt_barr_tbl)
        )
        self.barr_tbl = TreeviewTable(
            self.barr_fr, ("Barrel No", "Type", "Gallons", "Proof Gallons",
                           "Date Filled", "Age", "Investor")
        )
        self.barr_cfr = CommandFrame(self.barr_fr)
        self.barr_vfr = ViewFrame(self.barr_cfr, 'barrels', self.barr_tbl)
        self.barr_optfr = OptionFrame(self.barr_cfr)
        LogisticsButton(self.barr_optfr, "Add Barrel", 'barrels',
                         self.barr_tbl,
                         lambda:
                         AddView(self.master, 'barrels', self.barr_tbl, 1,
                                 self.barr_vfr, self.barr_count_fr)
        )
        LogisticsButton(self.barr_optfr, "Empty Barrel", 'barrels',
                         self.barr_tbl,
                         lambda:
                         selection_check('barrels', self.barr_tbl,
                                         self.barr_vfr, self.master,
                                         self.barr_count_fr, empty=True)
        )
        LogisticsButton(self.barr_optfr, "Update COGS", 'barrels',
                         self.barr_tbl,
                         lambda:
                         CogsView(self.master, 'estimated_cogs', self.barr_tbl,
                                  self.barr_vfr)
        )
        LogisticsButton(self.barr_optfr, "Edit Selection", 'barrels',
                         self.barr_tbl,
                         lambda:
                         selection_check('barrels', self.barr_tbl,
                                         self.barr_vfr, self.master,
                                         self.barr_count_fr)
        )
        LogisticsButton(self.barr_optfr, "Delete Selection", 'barrels',
                         self.barr_tbl,
                         lambda:
                         selection_check('barrels', self.barr_tbl,
                                         self.barr_vfr, self.master,
                                         self.barr_count_fr, delete=True)
        )
        self.barr_optfr.pack(pady=2)
        self.barr_count_fr = BarrelCountFrame(self.barr_cfr)
        self.barr_cfr.pack(padx=10)

        self.empt_barr_tbl = TreeviewTable(
            self.empt_barr_fr, ('Barrel No', 'Type', 'Gallons', 'PG',
                                'PG Leftover', 'Filled', 'Emptied', 'Age',
                                'Investor')
        )
        self.empt_barr_cfr = CommandFrame(self.empt_barr_fr)
        self.empt_barr_optfr = OptionFrame(self.empt_barr_cfr)
        LogisticsButton(self.empt_barr_optfr, "Edit Selection",
                         'empty_barrels', self.empt_barr_tbl,
                         lambda:
                         selection_check('empty_barrels', self.empt_barr_tbl,
                                         None, self.master, self.barr_count_fr)
        )
        LogisticsButton(self.empt_barr_optfr, "Delete Selection",
                         'empty_barrels', self.empt_barr_tbl,
                         lambda:
                         selection_check('empty_barrels', self.empt_barr_tbl,
                                         None, self.master, self.barr_count_fr,
                                         delete=True)
        )
        self.empt_barr_optfr.pack(pady=2)
        self.empt_barr_cfr.pack(padx=10)

        self.po_nb = ttk.Notebook(self.master, height=self.height,
                                  width=self.width)
        self.po_fr = tk.Frame(self.po_nb)
        self.po_nb.add(self.po_fr, text="Purchase Orders", padding=10)
        self.po_fr.bind(
            '<Visibility>',
            lambda event:
            self.po_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.pending_fr = tk.Frame(self.po_nb)
        self.po_nb.add(self.pending_fr, text="Pending Purchase Orders",
                       padding=10)
        self.pending_fr.bind(
            '<Visibility>',
            lambda event:
            self.pending_vfr.columns.event_generate("<<ComboboxSelected>>")
        )
        self.po_tbl = TreeviewTable(
            self.po_fr, ("PO Date", "PU Date", "Product", "Amount", "Unit",
                         "Price", "Total", "Destination","PO No.")
        )
        self.po_cfr = CommandFrame(self.po_fr)
        self.po_vfr = ViewFrame(self.po_cfr, 'purchase_orders', self.po_tbl)
        self.po_optfr = OptionFrame(self.po_cfr)
        LogisticsButton(self.po_optfr, "Create Purchase Order",
                         'purchase_orders', self.po_tbl,
                         lambda:
                         PurchaseOrderView(self.master)
        )
        LogisticsButton(self.po_optfr, "View Purchase Order",
                         'purchase_orders', self.po_tbl,
                         lambda:
                         selection_check(None, self.po_tbl, None, self.master,
                                         self.barr_count_fr, edit=False)
        )
        LogisticsButton(self.po_optfr, "Edit Selection", 'purchase_orders',
                         self.po_tbl,
                         lambda:
                         selection_check('purchase_orders', self.po_tbl,
                                         self.po_vfr, self.master,
                                         self.barr_count_fr)
        )
        LogisticsButton(self.po_optfr, "Delete Selection", 'purchase_orders',
                         self.po_tbl,
                         lambda:
                         selection_check('purchase_orders', self.po_tbl,
                                         self.po_vfr, self.master,
                                         self.barr_count_fr, delete=True)
        )
        self.po_optfr.pack()
        self.po_cfr.pack(padx=10)

        self.pending_tbl = TreeviewTable(
            self.pending_fr, ("Date", "Pick Up", "Product", "Amount", "Unit",
                              "Price", "Total", "Destination", "PO No.")
        )
        self.pending_cfr = CommandFrame(self.pending_fr)
        self.pending_vfr = ViewFrame(self.pending_cfr, 'pending_po',
                                      self.pending_tbl)
        self.pending_optfr = OptionFrame(self.pending_cfr)
        LogisticsButton(self.pending_optfr, "Fulfill Purchase Order",
                         'pending_po', self.pending_tbl,
                         lambda:
                         selection_check('pending_po', self.pending_tbl,
                                         self.pending_vfr, self.master,
                                         self.barr_count_fr, edit=False)
        )
        LogisticsButton(self.pending_optfr, "Edit Selection", 'pending_po',
                         self.pending_tbl,
                         lambda:
                         selection_check('pending_po', self.pending_tbl,
                                         self.pending_vfr, self.master,
                                         self.barr_count_fr)
        )
        LogisticsButton(self.pending_optfr, "Delete Selection", 'pending_po',
                         self.pending_tbl,
                         lambda:
                         selection_check('pending_po', self.pending_tbl,
                                         self.pending_vfr, self.master,
                                         self.barr_count_fr, delete=True)
        )
        self.pending_optfr.pack()
        self.pending_cfr.pack(padx=10)

        self.emptr_nb = ttk.Notebook(self.master, height=self.height,
                                     width=self.width)
        self.emptr_fr = tk.Frame(self.emptr_nb)
        self.emptr_nb.add(self.emptr_fr, text="Employee Transactions",
                          padding=10)
        self.emptr_tbl = TreeviewTable(
            self.emptr_fr, ("Date", "Product", "Amount", "Unit", "Employee",
                            "Destination")
        )
        self.emptr_cfr = CommandFrame(self.emptr_fr)
        self.emptr_optfr = OptionFrame(self.emptr_cfr)
        LogisticsButton(self.emptr_optfr, "Transaction",
                         'employee_transactions', self.emptr_tbl,
                         lambda:
                         EmptrView(self.master, 'employee_transactions',
                                   self.emptr_tbl)
        )
        LogisticsButton(self.emptr_optfr, "Edit Selection",
                         'employee_transactions', self.emptr_tbl,
                         lambda:
                         selection_check('employee_transactions',
                                         self.emptr_tbl, None,
                                         self.master, self.barr_count_fr)
        )
        LogisticsButton(self.emptr_optfr, "Delete Selection",
                         'employee_transactions', self.emptr_tbl,
                         lambda:
                         selection_check('employee_transactions',
                                         self.emptr_tbl, None,
                                         self.master, self.barr_count_fr,
                                         delete=True)
        )
        self.emptr_optfr.pack()
        self.emptr_cfr.pack(padx=10)

        self.reports_nb = ttk.Notebook(self.master, height=self.height,
                                       width=self.width)
        self.reports_fr = ReportsFrame(self.reports_nb)
        self.reports_nb.add(self.reports_fr, text="Monthly Report", padding=10)
        self.reports_fr.bind(
            "<Visibility>",
            lambda event:
            self.reports_fr.year_cmbo_box.event_generate("<<ComboboxSelected>>")
        )

        # Menubar at top of program
        self.menubar = tk.Menu(self.master)
        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        self.menu1.add_command(
            label="Raw Materials and Bottles",
            command=lambda:
            view_widget(self.master, self.bottinv_nb, 'bottom', 'raw_materials',
                        'All', 'All', self.raw_tbl)
        )
        self.menu1.add_command(
            label="Grain",
            command=lambda:
            view_widget(self.master, self.grain_nb, 'bottom', 'grain', 'All',
                        'All', self.grain_tbl)
        )
        self.menu1.add_command(
            label="Barrels",
            command=lambda:
            view_widget(self.master, self.barr_nb, 'bottom', 'barrels', 'All',
                        'All', self.barr_tbl)
        )
        self.menubar.add_cascade(label="Inventory", menu=self.menu1)

        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(
            label="Purchase Orders",
            command=lambda:
            view_widget(self.master, self.po_nb, 'bottom', 'purchase_orders',
                        'All', 'All', self.po_tbl)
        )
        self.menu2.add_command(
            label="Employee Transactions",
            command=lambda:
            view_widget(self.master, self.emptr_nb, 'bottom',
                        'employee_transactions', 'All', 'All', self.emptr_tbl)
        )
        self.menubar.add_cascade(label="Shipping and Transactions",
                                 menu=self.menu2)

        self.menu3 = tk.Menu(self.menubar, tearoff=0)
        self.menu3.add_command(
            label="Production Sheets",
            command=lambda:
            file_view("production_sheets", self.master)
        )
        self.menu3.add_command(
            label="Case Labels",
            command=lambda:
            file_view("case_labels", self.master)
        )
        self.menubar.add_cascade(label="Files", menu=self.menu3)

        self.menu4 = tk.Menu(self.menubar, tearoff=0)
        self.menu4.add_command(
            label="Monthly Reports",
            command=lambda:
            view_widget(self.master, self.reports_nb, 'bottom', None, 'All',
                        'All', None)
        )
        self.menu4.add_command(label="Export for Excel",
                               command=create_excel_inv)
        self.menubar.add_cascade(label="Analysis", menu=self.menu4)
        self.master.config(menu=self.menubar)

    def center_window(self):
        self.master.update_idletasks()
        width = self.width
        frm_width = self.master.winfo_rootx() - self.master.winfo_x()
        win_width = width + 2 * frm_width
        height = self.height
        titlebar_height = self.master.winfo_rooty() - self.master.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.master.winfo_screenwidth() // 2 - win_width // 2
        y = self.master.winfo_screenheight() // 2 - win_height // 2 - 20
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root = tk.Tk()
gui = Inventory(root)
root.mainloop()
