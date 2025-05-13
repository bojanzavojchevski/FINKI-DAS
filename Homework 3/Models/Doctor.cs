namespace HospitalAppointmentApp.Models
{
    public class Doctor
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public int HospitalId { get; set; }
        public Hospital Hospital { get; set; }

        public virtual ICollection<Patient> Patients { get; set; }
    }
}
