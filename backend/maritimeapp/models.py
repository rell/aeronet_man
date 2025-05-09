from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Max, Min


class Site(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    aeronet_number = models.IntegerField(default=0)
    description = models.TextField()
    span_date = ArrayField(
        models.DateField(),
        size=2,
        blank=True,
        null=True,
        help_text="Array holding the span of dates [start_date, end_date]",
    )

    def update_span_date(self):
        dates = DownloadAODDaily.objects.filter(cruise=self.name, level=15).aggregate(
            start_date=Min("date_DD_MM_YYYY"), end_date=Max("date_DD_MM_YYYY")
        )
        Site.objects.filter(pk=self.pk).update(
            span_date=[dates["start_date"], dates["end_date"]]
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_span_date()


"""
AP - HeaderCSV
Updated (02/06/25)
Date(dd:mm:yyyy),
Time(hh:mm:ss),
Air Mass,Latitude,
Longitude,
AOD_340nm,
AOD_380nm,
AOD_440nm,
AOD_500nm(int),
AOD_675nm,
AOD_870nm,
AOD_1020nm,
AOD_1640nm,
Water Vapor(cm),
440-870nm_Angstrom_Exponent,
Last_Processing_Date(dd:mm:yyyy),
AERONET_Number,
Microtops_Number
"""


class DownloadAODAP(models.Model):
    date_DD_MM_YYYY = models.DateField(db_index=True)
    time_HH_MM_SS = models.TimeField(db_index=False)
    air_mass = models.FloatField(default=-999.0)
    aod_340nm = models.FloatField(default=-999.0)
    aod_380nm = models.FloatField(default=-999.0)
    aod_440nm = models.FloatField(default=-999.0)
    aod_500nm = models.FloatField(default=-999.0)
    aod_675nm = models.FloatField(default=-999.0)
    aod_870nm = models.FloatField(default=-999.0)
    aod_1020nm = models.FloatField(default=-999.0)
    aod_1640nm = models.FloatField(default=-999.0)
    water_vapor_CM = models.FloatField(default=-999.0)
    angstrom_exponent_440_870 = models.FloatField(default=-999.0)
    last_processing_date_DD_MM_YYYY = models.DateField(db_index=True)
    aeronet_number = models.IntegerField(default=0)
    microtops_number = models.IntegerField(default=0)
    coordinates = gis_models.PointField(default=Point(0, 0))
    coordinates_wkt = models.CharField(max_length=255, blank=True, null=True)
    cruise = models.CharField(default="")
    level = models.IntegerField()
    pi = models.CharField(max_length=400, default="")
    pi_email = models.CharField(max_length=400, default="")

    class Meta:
        indexes = [
            models.Index(fields=["level", "cruise"]),
        ]


"""
Date(dd:mm:yyyy),
Time(hh:mm:ss),
Air Mass,
Latitude,
Longitude,
AOD_340nm,
AOD_380nm,
AOD_440nm,
AOD_500nm(int),
AOD_675nm,
AOD_870nm,
AOD_1020nm,
AOD_1640nm,
Water Vapor(cm),
440-870nm_Angstrom_Exponent,
STD_340nm,
STD_380nm,
STD_440nm,
STD_500nm(int),
STD_675nm,
STD_870nm,
STD_1020nm,
STD_1640nm,
STD_Water_Vapor(cm),
STD_440-870nm_Angstrom_Exponent,
Number_of_Observations,
Last_Processing_Date(dd:mm:yyyy),
AERONET_Number,
Microtops_Number
"""


class DownloadAODDaily(models.Model):
    date_DD_MM_YYYY = models.DateField(db_index=True)
    time_HH_MM_SS = models.TimeField(db_index=False)
    air_mass = models.FloatField(default=-999.0)
    aod_340nm = models.FloatField(default=-999.0)
    aod_380nm = models.FloatField(default=-999.0)
    aod_440nm = models.FloatField(default=-999.0)
    aod_500nm = models.FloatField(default=-999.0)
    aod_675nm = models.FloatField(default=-999.0)
    aod_870nm = models.FloatField(default=-999.0)
    aod_1020nm = models.FloatField(default=-999.0)
    aod_1640nm = models.FloatField(default=-999.0)
    water_vapor_CM = models.FloatField(default=-999.0)
    angstrom_exponent_440_870 = models.FloatField(default=-999.0)
    std_340nm = models.FloatField(default=-999.0)
    std_380nm = models.FloatField(default=-999.0)
    std_440nm = models.FloatField(default=-999.0)
    std_500nm = models.FloatField(default=-999.0)
    std_675nm = models.FloatField(default=-999.0)
    std_870nm = models.FloatField(default=-999.0)
    std_1020nm = models.FloatField(default=-999.0)
    std_1640nm = models.FloatField(default=-999.0)
    std_water_vapor_CM = models.FloatField(default=-999.0)
    std_angstrom_exponent_440_870 = models.FloatField(default=-999.0)
    number_of_observations = models.IntegerField(null=True, blank=True)
    last_processing_date_DD_MM_YYYY = models.DateField()
    aeronet_number = models.IntegerField(default=0)
    microtops_number = models.IntegerField(default=0)
    coordinates = gis_models.PointField(default=Point(0, 0))
    coordinates_wkt = models.CharField(max_length=255, blank=True, null=True)
    cruise = models.CharField(default="")
    level = models.IntegerField()
    pi = models.CharField(max_length=400, default="")
    pi_email = models.CharField(max_length=400, default="")

    class Meta:
        indexes = [
            models.Index(fields=["level", "cruise"]),
        ]


"""
Date(dd:mm:yyyy),
Time(hh:mm:ss),
Air Mass,
Latitude,
Longitude,
AOD_340nm,
AOD_380nm,
AOD_440nm,
AOD_500nm(int),
AOD_675nm,
AOD_870nm,
AOD_1020nm,
AOD_1640nm,
Water Vapor(cm),
440-870nm_Angstrom_Exponent,
STD_340nm,
STD_380nm,
STD_440nm,
STD_500nm(int),
STD_675nm,
STD_870nm,
STD_1020nm,
STD_1640nm,
STD_Water_Vapor(cm),
STD_440-870nm_Angstrom_Exponent,
Number_of_Observations,
Last_Processing_Date(dd:mm:yyyy),
AERONET_Number,
Microtops_Number
"""


class DownloadAODSeries(models.Model):
    date_DD_MM_YYYY = models.DateField(db_index=True)
    time_HH_MM_SS = models.TimeField(db_index=False)
    air_mass = models.FloatField(default=-999.0)
    aod_340nm = models.FloatField(default=-999.0)
    aod_380nm = models.FloatField(default=-999.0)
    aod_440nm = models.FloatField(default=-999.0)
    aod_500nm = models.FloatField(default=-999.0)
    aod_675nm = models.FloatField(default=-999.0)
    aod_870nm = models.FloatField(default=-999.0)
    aod_1020nm = models.FloatField(default=-999.0)
    aod_1640nm = models.FloatField(default=-999.0)
    water_vapor_CM = models.FloatField(default=-999.0)
    angstrom_exponent_440_870 = models.FloatField(default=-999.0)
    std_340nm = models.FloatField(default=-999.0)
    std_380nm = models.FloatField(default=-999.0)
    std_440nm = models.FloatField(default=-999.0)
    std_500nm = models.FloatField(default=-999.0)
    std_675nm = models.FloatField(default=-999.0)
    std_870nm = models.FloatField(default=-999.0)
    std_1020nm = models.FloatField(default=-999.0)
    std_1640nm = models.FloatField(default=-999.0)
    std_water_vapor_CM = models.FloatField(default=-999.0)
    std_angstrom_exponent_440_870 = models.FloatField(default=-999.0)
    number_of_observations = models.IntegerField(null=True, blank=True)
    last_processing_date_DD_MM_YYYY = models.DateField()
    aeronet_number = models.IntegerField(default=0)
    microtops_number = models.IntegerField(default=0)
    coordinates = gis_models.PointField(default=Point(0, 0))
    coordinates_wkt = models.CharField(max_length=255, blank=True, null=True)
    cruise = models.CharField(default="")
    level = models.IntegerField()
    pi = models.CharField(max_length=400, default="")
    pi_email = models.CharField(max_length=400, default="")

    class Meta:
        indexes = [
            models.Index(fields=["level", "cruise"]),
        ]


"""
Date(dd:mm:yyyy),
Time(hh:mm:ss),
Julian_Day,
Latitude,
Longitude,
Total_AOD_500nm(tau_a),
Fine_Mode_AOD_500nm(tau_f),
Coarse_Mode_AOD_500nm(tau_c),
FineModeFraction_500nm(eta),
CoarseModeFraction_500nm(1_eta),
2nd_Order_Reg_Fit_Error_Total_AOD_500nm(regression_dtau_a),
RMSE_Fine_Mode_AOD_500nm(Dtau_f),
RMSE_Coarse_Mode_AOD_500nm(Dtau_c),
RMSE_FMF_and_CMF_Fractions_500nm(Deta),
Angstrom_Exponent(AE)_Total_500nm(alpha),
dAE/dln(wavelength)_Total_500nm(alphap),
AE_Fine_Mode_500nm(alpha_f),
dAE/dln(wavelength)_Fine_Mode_500nm(alphap_f),
Solar_Zenith_Angle,
Air_Mass,
870nm_Input_AOD,
675nm_Input_AOD,
500nm(int)_Input_AOD,
440nm_Input_AOD,
380nm_Input_AOD,
Last_Processing_Date(dd:mm:yyyy),
AERONET_Number,
Microtops_Number
"""


class DownloadSDAAP(models.Model):
    date_DD_MM_YYYY = models.DateField(db_index=True)
    time_HH_MM_SS = models.TimeField(db_index=False)
    julian_day = models.FloatField(null=True, blank=True, default=-999.0)
    total_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    coarse_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    fine_mode_fraction_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    coarse_mode_fraction_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    regression_dtau_a = models.FloatField(null=True, blank=True, default=-999.0)
    rmse_fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    rmse_coarse_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    rmse_fmf_and_cmf_fractions_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    angstrom_exponent_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    dae_dln_wavelength_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    ae_fine_mode_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    dae_dln_wavelength_fine_mode_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    solar_zenith_angle = models.FloatField(null=True, blank=True, default=-999.0)
    air_mass = models.FloatField(null=True, blank=True, default=-999.0)
    aod_870nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_675nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_440nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_380nm = models.FloatField(null=True, blank=True, default=-999.0)
    last_processing_date_DD_MM_YYYY = models.DateField(null=True, blank=True)
    aeronet_number = models.IntegerField(null=True, blank=True)
    microtops_number = models.IntegerField(null=True, blank=True)
    coordinates = gis_models.PointField(default=Point(0, 0))
    coordinates_wkt = models.CharField(max_length=255, blank=True, null=True)
    cruise = models.CharField(default="")
    solar_zenith_angle = models.FloatField(null=True, blank=True, default=-999.0)
    level = models.IntegerField()
    pi = models.CharField(max_length=400, default="")
    pi_email = models.CharField(max_length=400, default="")

    class Meta:
        indexes = [
            models.Index(fields=["level", "cruise"]),
        ]


"""
Date(dd:mm:yyyy),
Time(hh:mm:ss),
Julian_Day,
Latitude,
Longitude,
Total_AOD_500nm(tau_a),
Fine_Mode_AOD_500nm(tau_f),
Coarse_Mode_AOD_500nm(tau_c),
FineModeFraction_500nm(eta),
CoarseModeFraction_500nm(1_eta),
2nd_Order_Reg_Fit_Error_Total_AOD_500nm(regression_dtau_a),
RMSE_Fine_Mode_AOD_500nm(Dtau_f),
RMSE_Coarse_Mode_AOD_500nm(Dtau_c),
RMSE_FMF_and_CMF_Fractions_500nm(Deta),
Angstrom_Exponent(AE)_Total_500nm(alpha),
dAE/dln(wavelength)_Total_500nm(alphap),
AE_Fine_Mode_500nm(alpha_f),
dAE/dln(wavelength)_Fine_Mode_500nm(alphap_f),
870nm_Input_AOD,675nm_Input_AOD,
500nm(int)_Input_AOD,
440nm_Input_AOD,
380nm_Input_AOD,
STDEV-Total_AOD_500nm(tau_a),
STDEV-Fine_Mode_AOD_500nm(tau_f),
STDEV-Coarse_Mode_AOD_500nm(tau_c),
STDEV-FineModeFraction_500nm(eta),
STDEV-CoarseModeFraction_500nm(1_eta),
STDEV-2nd_Order_Reg_Fit_Error_Total_AOD_500nm(regression_dtau_a),
STDEV-RMSE_Fine_Mode_AOD_500nm(Dtau_f),
STDEV-RMSE_Coarse_Mode_AOD_500nm(Dtau_c),
STDEV-RMSE_FMF_and_CMF_Fractions_500nm(Deta),
STDEV-Angstrom_Exponent(AE)_Total_500nm(alpha),
STDEV-dAE/dln(wavelength)_Total_500nm(alphap),
STDEV-AE_Fine_Mode_500nm(alpha_f),
STDEV-dAE/dln(wavelength)_Fine_Mode_500nm(alphap_f),
STDEV-870nm_Input_AOD,
STDEV-675nm_Input_AOD,
STDEV-500nm(int)_Input_AOD,
STDEV-440nm_Input_AOD,
STDEV-380nm_Input_AOD,
Number_of_Observations,
Last_Processing_Date(dd:mm:yyyy),
AERONET_Number,
Microtops_Number
"""


class DownloadSDADaily(models.Model):
    date_DD_MM_YYYY = models.DateField(db_index=True)
    time_HH_MM_SS = models.TimeField(db_index=False)
    julian_day = models.FloatField(null=True, blank=True, default=-999.0)
    total_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    coarse_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    fine_mode_fraction_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    coarse_mode_fraction_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    regression_dtau_a = models.FloatField(null=True, blank=True, default=-999.0)
    rmse_fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    rmse_coarse_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    rmse_fmf_and_cmf_fractions_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    angstrom_exponent_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    dae_dln_wavelength_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    ae_fine_mode_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    dae_dln_wavelength_fine_mode_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    aod_870nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_675nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_440nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_380nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_total_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_coarse_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_fine_mode_fraction_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_coarse_mode_fraction_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_regression_dtau_a = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_rmse_fine_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_rmse_coarse_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_rmse_fmf_and_cmf_fractions_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_angstrom_exponent_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_dae_dln_wavelength_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_ae_fine_mode_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_dae_dln_wavelength_fine_mode_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )

    stdev_aod_870nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_675nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_440nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_380nm = models.FloatField(null=True, blank=True, default=-999.0)
    number_of_observations = models.IntegerField(null=True, blank=True)
    last_processing_date_DD_MM_YYYY = models.DateField(null=True, blank=True)
    aeronet_number = models.IntegerField(null=True, blank=True)
    microtops_number = models.IntegerField(null=True, blank=True)
    coordinates = gis_models.PointField(default=Point(0, 0))
    coordinates_wkt = models.CharField(max_length=255, blank=True, null=True)
    cruise = models.CharField(default="")
    level = models.IntegerField()
    pi = models.CharField(max_length=400, default="")
    pi_email = models.CharField(max_length=400, default="")

    class Meta:
        indexes = [
            models.Index(fields=["level", "cruise"]),
        ]


class DownloadSDASeries(models.Model):
    date_DD_MM_YYYY = models.DateField(db_index=True)
    time_HH_MM_SS = models.TimeField(db_index=False)
    julian_day = models.FloatField(null=True, blank=True, default=-999.0)
    total_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    coarse_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    fine_mode_fraction_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    coarse_mode_fraction_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    regression_dtau_a = models.FloatField(null=True, blank=True, default=-999.0)
    rmse_fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    rmse_coarse_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    rmse_fmf_and_cmf_fractions_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    angstrom_exponent_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    dae_dln_wavelength_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    ae_fine_mode_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    dae_dln_wavelength_fine_mode_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    aod_870nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_675nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_440nm = models.FloatField(null=True, blank=True, default=-999.0)
    aod_380nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_total_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_fine_mode_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_coarse_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_fine_mode_fraction_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_coarse_mode_fraction_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_regression_dtau_a = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_rmse_fine_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_rmse_coarse_mode_aod_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_rmse_fmf_and_cmf_fractions_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_angstrom_exponent_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_dae_dln_wavelength_total_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )
    stdev_ae_fine_mode_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_dae_dln_wavelength_fine_mode_500nm = models.FloatField(
        null=True, blank=True, default=-999.0
    )

    stdev_aod_870nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_675nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_500nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_440nm = models.FloatField(null=True, blank=True, default=-999.0)
    stdev_aod_380nm = models.FloatField(null=True, blank=True, default=-999.0)
    number_of_observations = models.IntegerField(null=True, blank=True)
    last_processing_date_DD_MM_YYYY = models.DateField(null=True, blank=True)
    aeronet_number = models.IntegerField(null=True, blank=True)
    microtops_number = models.IntegerField(null=True, blank=True)
    coordinates = gis_models.PointField(default=Point(0, 0))
    coordinates_wkt = models.CharField(max_length=255, blank=True, null=True)
    cruise = models.CharField(default="")
    level = models.IntegerField()
    pi = models.CharField(max_length=400, default="")
    pi_email = models.CharField(max_length=400, default="")

    class Meta:
        indexes = [
            models.Index(fields=["level", "cruise"]),
        ]


class TableHeader(models.Model):
    freq = models.CharField(max_length=255, default="")
    datatype = models.CharField(max_length=255)
    level = models.IntegerField()
    base_header_l1 = models.CharField(
        max_length=9999
    )  # NOTE: Ex. Version 3; LEVEL 1.0 Maritime Aerosol Network (MAN) Measurements: These data are not screened and may not have final calibration applied
    base_header_l2 = models.CharField(
        max_length=9999
    )  # NOTE: Ex. Due to the research and development phase characterizing AERONET-MAN; use of data requires offering co-authorship to Principal Investigators.

    # NOTE: Header should now be grabbed from table and reverse translated using original keys

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["datatype", "level", "freq"], name="unique_dataType_level"
            )
        ]
