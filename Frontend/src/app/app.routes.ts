import { Routes } from '@angular/router';
import { NotFoundComponent } from './components/common/not-found/not-found.component';
import { AnalyticsComponent } from './components/dashboard/analytics/analytics.component';
import { CryptoComponent } from './components/dashboard/crypto/crypto.component';
import { PUsersComponent } from './components/projects/p-users/p-users.component';
import { AnalyticsPageComponent } from './components/pages/analytics-page/analytics-page.component';
import { AnalyticsCustomersComponent } from './components/pages/analytics-page/analytics-customers/analytics-customers.component';
import { AnalyticsReportsComponent } from './components/pages/analytics-page/analytics-reports/analytics-reports.component';
import { IconsComponent } from './components/pages/icons/icons.component';
import { FlaticonComponent } from './components/pages/icons/flaticon/flaticon.component';
import { RemixiconComponent } from './components/pages/icons/remixicon/remixicon.component';
import { MaterialSymbolsComponent } from './components/pages/icons/material-symbols/material-symbols.component';
import { MaterialIconsComponent } from './components/pages/icons/material-icons/material-icons.component';
import { TablesComponent } from './components/tables/tables.component';
import { BasicTableComponent } from './components/tables/basic-table/basic-table.component';
import { DataTableComponent } from './components/tables/data-table/data-table.component';
import { FormsComponent } from './components/forms/forms.component';
import { BasicFormComponent } from './components/forms/basic-form/basic-form.component';
import { WizardFormComponent } from './components/forms/wizard-form/wizard-form.component';
import { AdvancedFormComponent } from './components/forms/advanced-form/advanced-form.component';
import { EditorsComponent } from './components/forms/editors/editors.component';
import { FileUploaderComponent } from './components/forms/file-uploader/file-uploader.component';
import { AuthenticationComponent } from './components/authentication/authentication.component';
import { LoginComponent } from './components/authentication/login/login.component';
import { RegisterComponent } from './components/authentication/register/register.component';
import { ForgotPasswordComponent } from './components/authentication/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './components/authentication/reset-password/reset-password.component';
import { SigninSignupComponent } from './components/authentication/signin-signup/signin-signup.component';
import { LogoutComponent } from './components/authentication/logout/logout.component';
import { ConfirmMailComponent } from './components/authentication/confirm-mail/confirm-mail.component';
import { LockScreenComponent } from './components/authentication/lock-screen/lock-screen.component';
import { InternalErrorComponent } from './components/common/internal-error/internal-error.component';
import { NotificationsComponent } from './components/pages/notifications/notifications.component';
import { AccountComponent } from './components/pages/account/account.component';
import { SecurityComponent } from './components/pages/security/security.component';
import { ConnectionsComponent } from './components/pages/connections/connections.component';
import { PrivacyPolicyComponent } from './components/pages/privacy-policy/privacy-policy.component';
import { ChartsComponent } from './components/charts/charts.component';
import { ApexchartsComponent } from './components/charts/apexcharts/apexcharts.component';
import { EchartsComponent } from './components/charts/echarts/echarts.component';
import { ChartjsComponent } from './components/charts/chartjs/chartjs.component';
import { UiKitComponent } from './components/ui-kit/ui-kit.component';
import { AlertsComponent } from './components/ui-kit/alerts/alerts.component';
import { AutocompleteComponent } from './components/ui-kit/autocomplete/autocomplete.component';
import { AvatarsComponent } from './components/ui-kit/avatars/avatars.component';
import { AccordionComponent } from './components/ui-kit/accordion/accordion.component';
import { BadgesComponent } from './components/ui-kit/badges/badges.component';
import { BreadcrumbComponent } from './components/ui-kit/breadcrumb/breadcrumb.component';
import { ButtonToggleComponent } from './components/ui-kit/button-toggle/button-toggle.component';
import { ButtonsComponent } from './components/ui-kit/buttons/buttons.component';
import { CardsComponent } from './components/ui-kit/cards/cards.component';
import { CarouselsComponent } from './components/ui-kit/carousels/carousels.component';
import { CheckboxComponent } from './components/ui-kit/checkbox/checkbox.component';
import { ChipsComponent } from './components/ui-kit/chips/chips.component';
import { ColorPickerComponent } from './components/ui-kit/color-picker/color-picker.component';
import { DatepickerComponent } from './components/ui-kit/datepicker/datepicker.component';
import { DialogComponent } from './components/ui-kit/dialog/dialog.component';
import { DividerComponent } from './components/ui-kit/divider/divider.component';
import { DragDropComponent } from './components/ui-kit/drag-drop/drag-drop.component';
import { ExpansionComponent } from './components/ui-kit/expansion/expansion.component';
import { FormFieldComponent } from './components/ui-kit/form-field/form-field.component';
import { GridComponent } from './components/ui-kit/grid/grid.component';
import { ImagesComponent } from './components/ui-kit/images/images.component';
import { InputComponent } from './components/ui-kit/input/input.component';
import { ListComponent } from './components/ui-kit/list/list.component';
import { ListboxComponent } from './components/ui-kit/listbox/listbox.component';
import { MenusComponent } from './components/ui-kit/menus/menus.component';
import { PaginationComponent } from './components/ui-kit/pagination/pagination.component';
import { ProgressBarComponent } from './components/ui-kit/progress-bar/progress-bar.component';
import { RadioComponent } from './components/ui-kit/radio/radio.component';
import { SelectComponent } from './components/ui-kit/select/select.component';
import { SidenavComponent } from './components/ui-kit/sidenav/sidenav.component';
import { SlideToggleComponent } from './components/ui-kit/slide-toggle/slide-toggle.component';
import { SliderComponent } from './components/ui-kit/slider/slider.component';
import { SpacingComponent } from './components/ui-kit/spacing/spacing.component';
import { SnackbarComponent } from './components/ui-kit/snackbar/snackbar.component';
import { StepperComponent } from './components/ui-kit/stepper/stepper.component';
import { TableComponent } from './components/ui-kit/table/table.component';
import { TabsComponent } from './components/ui-kit/tabs/tabs.component';
import { ToolbarComponent } from './components/ui-kit/toolbar/toolbar.component';
import { TooltipComponent } from './components/ui-kit/tooltip/tooltip.component';
import { TreeComponent } from './components/ui-kit/tree/tree.component';
import { TypographyComponent } from './components/ui-kit/typography/typography.component';
import { VideosComponent } from './components/ui-kit/videos/videos.component';
// Buy Gold
import { BuyGoldComponent } from './components/pages/buy-gold/buy-gold.component';
// Sell Gold
import { SellGoldComponent } from './components/pages/sell-gold/sell-gold.component';
import { authGuard } from './components/Guard/auth.guard';



export const routes: Routes = [
    {path:'', component:CryptoComponent},
    {path: 'analytics', component: AnalyticsComponent},
    {path: 'crypto', component: CryptoComponent},
    {path: 'users',component: PUsersComponent},
    {path: 'buy',component: BuyGoldComponent},
    {path: 'sell',component: SellGoldComponent},
    {
        path: 'analytics-page',
        component: AnalyticsPageComponent,
        children: [
            {path: '', component: AnalyticsCustomersComponent},
            {path: 'reports', component: AnalyticsReportsComponent}
        ]
    },
    {
        path: 'icons',
        component: IconsComponent,
        children: [
            {path: '', component: FlaticonComponent},
            {path: 'remixicon', component: RemixiconComponent},
            {path: 'material-symbols', component: MaterialSymbolsComponent},
            {path: 'material', component: MaterialIconsComponent}
        ]
    },
    {
        path: 'ui-kit',
        component: UiKitComponent,
        children: [
            {path: '', component: AlertsComponent},
            {path: 'autocomplete', component: AutocompleteComponent},
            {path: 'avatars', component: AvatarsComponent},
            {path: 'accordion', component: AccordionComponent},
            {path: 'badges', component: BadgesComponent},
            {path: 'breadcrumb', component: BreadcrumbComponent},
            {path: 'button-toggle', component: ButtonToggleComponent},
            {path: 'buttons', component: ButtonsComponent},
            {path: 'cards', component: CardsComponent},
            {path: 'carousels', component: CarouselsComponent},
            {path: 'checkbox', component: CheckboxComponent},
            {path: 'chips', component: ChipsComponent},
            {path: 'color-picker', component: ColorPickerComponent},
            {path: 'datepicker', component: DatepickerComponent},
            {path: 'dialog', component: DialogComponent},
            {path: 'divider', component: DividerComponent},
            {path: 'drag-drop', component: DragDropComponent},
            {path: 'expansion', component: ExpansionComponent},
            {path: 'form-field', component: FormFieldComponent},
            {path: 'grid', component: GridComponent},
            {path: 'images', component: ImagesComponent},
            {path: 'input', component: InputComponent},
            {path: 'list', component: ListComponent},
            {path: 'listbox', component: ListboxComponent},
            {path: 'menus', component: MenusComponent},
            {path: 'pagination', component: PaginationComponent},
            {path: 'progress-bar', component: ProgressBarComponent},
            {path: 'radio', component: RadioComponent},
            {path: 'select', component: SelectComponent},
            {path: 'sidenav', component: SidenavComponent},
            {path: 'slide-toggle', component: SlideToggleComponent},
            {path: 'slider', component: SliderComponent},
            {path: 'spacing', component: SpacingComponent},
            {path: 'snackbar', component: SnackbarComponent},
            {path: 'stepper', component: StepperComponent},
            {path: 'table', component: TableComponent},
            {path: 'tabs', component: TabsComponent},
            {path: 'toolbar', component: ToolbarComponent},
            {path: 'tooltip', component: TooltipComponent},
            {path: 'tree', component: TreeComponent},
            {path: 'typography', component: TypographyComponent},
            {path: 'videos', component: VideosComponent}
        ]
    },
    {
        path: 'tables',
        component: TablesComponent,
        children: [
            {path: '', component: BasicTableComponent},
            {path: 'data', component: DataTableComponent}
        ]
    },
    {
        path: 'charts',
        component: ChartsComponent,
        children: [
            {path: '', component: ApexchartsComponent},
            {path: 'echarts', component: EchartsComponent},
            {path: 'chartjs', component: ChartjsComponent}
        ]
    },
    {
        path: 'forms',
        component: FormsComponent,
        children: [
            {path: '', component: BasicFormComponent},
            {path: 'wizard', component: WizardFormComponent},
            {path: 'advanced', component: AdvancedFormComponent},
            {path: 'editors', component: EditorsComponent},
            {path: 'file-uploader', component: FileUploaderComponent}
        ]
    },
    {
        path: 'authentication',
        component: AuthenticationComponent,
        canActivate: [authGuard],
        children: [
            {path: '', component: LoginComponent},
            {path: 'register', component: RegisterComponent},
            {path: 'forgot-password', component: ForgotPasswordComponent},
            {path: 'reset-password', component: ResetPasswordComponent},
            {path: 'signin-signup', component: SigninSignupComponent},
            {path: 'logout', component: LogoutComponent},
            {path: 'confirm-mail', component: ConfirmMailComponent},
            {path: 'lock-screen', component: LockScreenComponent}
        ]
    },
    {path: 'error-500', component: InternalErrorComponent},
    {path: 'notifications', component: NotificationsComponent},
    {path: 'account', component: AccountComponent},
    {path: 'security', component: SecurityComponent},
    {path: 'connections', component: ConnectionsComponent},
    {path: 'privacy-policy', component: PrivacyPolicyComponent},
    // Here add new pages component

    {path: '**', component: NotFoundComponent} // This line will remain down from the whole pages component list
];