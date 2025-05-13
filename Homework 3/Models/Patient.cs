using System.ComponentModel.DataAnnotations;

namespace HospitalAppointmentApp.Models
{
    public enum Gender
    {
        Male,
        Female
    }
    public class Patient
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Името е задолжително")]
        public string Name { get; set; }


        [Display(Name = "Код на пациентот")]
        [RegularExpression(@"^\d{5}$", ErrorMessage = "Кодот мора да биде точно 5 цифри")]
        public string PatientCode { get; set; }


        public Gender Gender { get; set; }

        public virtual ICollection<Doctor> Doctors { get; set; }
    }
}
